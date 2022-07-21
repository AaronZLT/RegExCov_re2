import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys
import os
import logging
import shutil
from LogUtils import createLog,closeLog
ws="/home/peipei/RepoReaper/" ##workspace
file_dir="/home/peipei/RepoReaper/RegexCollection/"
log_dir="/home/peipei/RepoReaper/loggings/"
agent_jar="/home/peipei/RepoReaper/AssistInstrumentation/javassist-instrument.jar"
# ws="/home/pwang7/RepoReaper/" ##workspace
# file_dir="/home/pwang7/results/"
# log_dir="/home/pwang7/log/"
# agent_jar="/home/pwang7/code/javassist-instrument.jar"
ns="http://maven.apache.org/POM/4.0.0"

arg_prefix='''-javaagent:'''+agent_jar+'''='''+log_dir

def buildSureFirePlugin(arg_agent,version="2.18"):
    print("build sure fire plugin arg_agent: ",arg_agent)
    plugin=ET.Element("plugin")
    ET.SubElement(plugin,"groupId").text="org.apache.maven.plugins"
    ET.SubElement(plugin,"artifactId").text="maven-surefire-plugin"
    ET.SubElement(plugin,"version").text=version
    configuraton=ET.SubElement(plugin,"configuration")
    ET.SubElement(configuraton,"skipTests").text="false"
    ET.SubElement(configuraton,"argLine").text=arg_agent
    ET.SubElement(configuraton,"testFailureIgnore").text="true"
    ET.SubElement(configuraton,"perCoreThreadCount").text="false"
    ET.SubElement(configuraton,"parallel").text="all"
    ET.SubElement(configuraton,"threadCount").text="1"

    return plugin
#     <!-- executes maven test with -javaagent option -->
#     <plugin>
#         <groupId>org.apache.maven.plugins</groupId>
#         <artifactId>maven-surefire-plugin</artifactId>
#         <version>2.14</version>
#         <configuration>
#                 <skipTests>false</skipTests>
#                 <argLine>-javaagent:target/${project.build.finalName}.jar=testUserLog</argLine>
#         </configuration>
#     </plugin>
def updateSurefirePlugin(maven_surefire,arg_agent): 
    print("update sure fire plugin arg_agent: ",arg_agent)
    version=maven_surefire.find("{%s}version"%ns)
    if version is not None and version.text=="2.20":
        version.text="2.18"
         
    config=maven_surefire.find("{%s}configuration"%ns)
    if config is None:
        config=ET.Element("configuration")
        maven_surefire.append(config)
    
    
    skip=config.find("{%s}skip"%ns)
    if skip is not None:
        config.remove(skip)
    skipTests=config.find("{%s}skipTests"%ns)
    if skipTests is None:
        skipTests=ET.SubElement(config,"skipTests")
    skipTests.text="false"
    
    argLine=config.find("{%s}argLine"%ns)
    if argLine is None:
        argLine=ET.SubElement(config,"argLine")
        argLine.text=arg_agent
    elif argLine.text is None:
        argLine.text=arg_agent
    elif arg_agent not in argLine.text:
        argLine.text=argLine.text+" "+arg_agent
    
    testFailureIgnore=config.find("{%s}testFailureIgnore"%ns)
    if testFailureIgnore is None:
        testFailureIgnore=ET.SubElement(config,"testFailureIgnore")
    testFailureIgnore.text="true"
    
    perCoreThreadCount=config.find("{%s}perCoreThreadCount"%ns)
    if perCoreThreadCount is None:
        perCoreThreadCount=ET.SubElement(config,"perCoreThreadCount")
    perCoreThreadCount.text="false"
    
    parallel=config.find("{%s}parallel"%ns)
    if parallel is None:
        parallel=ET.SubElement(config,"parallel")
    parallel.text="all"
    
    threadCount=config.find("{%s}threadCount"%ns)
    if threadCount is None:
        threadCount=ET.SubElement(config,"threadCount")
    threadCount.text="1"
def updateDepVersion(dep,version):
    e_version=dep.find("{%s}version"%ns)
    if e_version is not None:
        e_version.text=version
    else:
        ET.SubElement(dep,"version").text=version  
              
def buildDep(groupId,artifactId,version,scope):
    dependency=ET.Element("dependency")
    ET.SubElement(dependency,"groupId").text=groupId
    ET.SubElement(dependency,"artifactId").text=artifactId
    ET.SubElement(dependency,"version").text=version
    ET.SubElement(dependency,"scope").text=scope
    return dependency

def buildDep2(groupId,artifactId,version):
    dependency=ET.Element("dependency")
    ET.SubElement(dependency,"groupId").text=groupId
    ET.SubElement(dependency,"artifactId").text=artifactId
    ET.SubElement(dependency,"version").text=version
    return dependency
#     <dependency>
#         <groupId>org.javassist</groupId>
#         <artifactId>javassist</artifactId>
#         <version>3.14.0-GA</version>
#     </dependency>

def getPomTree(pom_file):
    if not os.path.exists(pom_file):
        print("pom file: ",pom_file, " do not exist")

    print("pom file: ",pom_file)
    global ns
    tree = ET.ElementTree()
    tree.parse(pom_file)
    pom_root=tree.getroot()
    ns=pom_root.tag[1:-8]
    ET.register_namespace('', ns)
    return pom_root


def getJdkVersionFromProperties(properties):
    jdk=properties.find("{%s}jdk.version" % ns)       
    if jdk is not None and jdk.text.startswith("1."):
        return jdk.text
    jdk=properties.find("{%s}java.version" % ns)       
    if jdk is not None and jdk.text.startswith("1."):
        return jdk.text
              
    
    javac=properties.find("{%s}java.source.version" % ns)       
    if javac is not None and javac.text.startswith("1."):
        return javac.text     
       
    mvn_javac=properties.find("{%s}maven.compiler.source" % ns)       
    if mvn_javac is not None and mvn_javac.text.startswith("1."):
        return mvn_javac.text  
         
    mvn_java=properties.find("{%s}maven.compiler.target" % ns)       
    if mvn_java is not None and mvn_java.text.startswith("1."):
        return mvn_java.text
    return None

def getJdkVersionFromPlugins(plugins):
    for plugin in plugins:
            artifactId=plugin.find("{%s}artifactId" % ns).text
            conf=plugin.find("{%s}configuration" % ns)
            if artifactId=='maven-compiler-plugin' and conf is not None:
                conf_javac=conf.find("{%s}source" % ns)
                if conf_javac is not None and conf_javac.text is not None and conf_javac.text.startswith("1."):
                    return conf_javac.text
    return None

def getJdkVersionFromBuild(build):
    build_plugins=build.find("{%s}plugins" % ns)
    if build_plugins is not None:
        plugins=build_plugins.findall("{%s}plugin" % ns)
        if plugins is not None:
            v=getJdkVersionFromPlugins(plugins)
            if v is not None:
                return v
        
    build_pluginManagement=build.find("{%s}pluginManagement" % ns)
    if build_pluginManagement is not None:
        build_plugins2=build_pluginManagement.find("{%s}plugins" % ns)
        if build_plugins2 is not None:
            plugins2=build_plugins2.findall("{%s}plugin" % ns)
            if plugins2 is not None:
                v=getJdkVersionFromPlugins(plugins2)
                if v is not None:
                    return v    
    return None
def getJdkVersionFromProfile(profiles):
    for profile in profiles:
            activation=profile.find("{%s}activation" % ns)
            if activation is not None:
                jdk=activation.find("{%s}jdk" % ns)
                if jdk is not None and jdk.text.startswith("1."):
                    return jdk.text
                
                build=profile.find("{%s}build" % ns)
                if build is not None:
                    v=getJdkVersionFromBuild(build)
                    if v is not None:
                        return v
    return None

def getJdkVersion(pom_root):
    print(pom_root) 
    properties=pom_root.find("{%s}properties" % ns)
    if properties is not None:
        res=getJdkVersionFromProperties(properties)
        if res is not None:
            return res
    
    build=pom_root.find("{%s}build" % ns) ##project build
    if build is not None:
        res=getJdkVersionFromBuild(build)
        if res is not None:
            return res
    
    project_profiles=pom_root.find("{%s}profiles" % ns)
    if project_profiles is not None:
        profiles=project_profiles.findall("{%s}profile" % ns)
        res=getJdkVersionFromProfile(profiles)
        if res is not None:
            return res
        
    return None 
                
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    fine_string=b'\n'.join([s for s in rough_string.splitlines() if s.strip()])
    reparsed = minidom.parseString(fine_string)
#     return reparsed.toprettyxml(indent="  ")
    find_string=reparsed.toprettyxml(indent="  ")
    fine_string='\n'.join([s for s in find_string.splitlines() if s.strip()])
    return fine_string

def buildToolChainPlugin(jdk_version):
    plugin=ET.Element("plugin")
    ET.SubElement(plugin,"groupId").text="org.apache.maven.plugins"
    ET.SubElement(plugin,"artifactId").text="maven-toolchains-plugin"
    ET.SubElement(plugin,"version").text="1.1"
    executions=ET.SubElement(plugin,"executions")
    execution=ET.SubElement(executions,"execution")
    goals=ET.SubElement(execution,"goals")
    ET.SubElement(goals,"goal").text="toolchain"
    configuraton=ET.SubElement(plugin,"configuration")
    toolchains=ET.SubElement(configuraton,"toolchains")
    jdk=ET.SubElement(toolchains,"jdk")
    ET.SubElement(jdk,"version").text="["+jdk_version+",)"
    
    tree = prettify(plugin)
    print(tree)
    return plugin
#     <plugin>
#         <groupId>org.apache.maven.plugins</groupId>
#         <artifactId></artifactId>
#         <version>1.1</version>
#         <executions>
#             <execution>
#                 <goals>
#                     <goal>toolchain</goal>
#                 </goals>
#             </execution>
#         </executions>
#         <configuration>
#             <toolchains>
#                 <jdk>
#                     <version>[1.8]</version>
#                 </jdk>
#             </toolchains>
#         </configuration>
#     </plugin>
 
def buildProfile():
    profile=ET.Element("profile")   
    #<id>agent</id>
    #<activation>
    #    <activeByDefault>true</activeByDefault>
    #</activation>
    ET.SubElement(profile,"id").text="agent"
    activation=ET.SubElement(profile,"activation")
    ET.SubElement(activation,"activeByDefault").text="true"
        
    build=ET.SubElement(profile,"build")
    plugins=ET.SubElement(build,"plugins")
    plugins.append(buildSureFirePlugin())
    
    dependencies=ET.SubElement(profile,"dependencies")
    dependencies.append(buildDep("org.hamcrest","hamcrest-core","1.3"))
    dependencies.append(buildDep("org.hamcrest","hamcrest-library","1.3"))
    dependencies.append(buildDep("org.mockito","mockito-all","1.9.5"))
    dependencies.append(buildDep("junit","junit","4.11"))
    dependencies.append(buildDep2("org.ow2.asm","asm","4.1","test"))
    dependencies.append(buildDep2("org.javassist","javassist","3.14.0-GA","test"))
    
    return profile
        
def updateProfile(profile):
    ##check if surefire exits
    build=profile.find("{%s}build"%ns)
    if build is not None:
        build_plugins=build.find("{%s}plugins"%ns)
        if build_plugins is not None:
            plugins=build_plugins.findall("{%s}plugin"%ns)
            artifactIds=[getArtifactId(plugin) for plugin in plugins]
            if "maven-surefire-plugin" in artifactIds:
                updateSurefirePlugin(plugins[artifactIds.index("maven-surefire-plugin")])
            else:
                plugins.append(buildSureFirePlugin())
    ##check dependencies
    profile_dependencies=profile.find("{%s}dependencies"%ns)
    if profile_dependencies is None:
        profile_dependencies=ET.SubElement(profile,"dependencies")
    validDep(profile_dependencies)
    
def getArtifactId(ele):
    return ele.find("{%s}artifactId"%ns).text

def validDep(deps):
    dependencies=deps.findall("{%s}dependency" % ns)
    artifactIds=[getArtifactId(dep) for dep in dependencies]
    
    if "junit" not in artifactIds:
        deps.append(buildDep2("junit","junit","4.12"))
    if "hamcrest-core" not in artifactIds:
        deps.append(buildDep2("org.hamcrest","hamcrest-core","1.3"))
    if "hamcrest-library" not in artifactIds:
        deps.append(buildDep2("org.hamcrest","hamcrest-library","1.3"))
    
    if "mockito-all" not in artifactIds:
        deps.append(buildDep2("org.mockito","mockito-all","1.9.5"))
        
    if "asm" not in artifactIds:
        deps.append(buildDep("org.ow2.asm","asm","4.1","test"))        
    if "javassist" not in artifactIds:
        deps.append(buildDep("org.javassist","javassist","3.18.1-GA","test")) ###3.14.0-GA for jdk1.7 3.18.1-GA works for jdk1.8
    else:
        dep=dependencies[artifactIds.index("javassist")]
        updateDepVersion(dep,"3.18.1-GA");

def validDeps(pom_root):
    project_dependencies=pom_root.find("{%s}dependencies" % ns)    
    if project_dependencies is None:
        project_dependencies=ET.Element("dependencies")
        pom_root.append(project_dependencies)  ##child pom inherit parent pom dependencies
        
    validDep(project_dependencies)
    
    proj_depManagement=pom_root.find("{%s}dependencyManagement" % ns)
    if proj_depManagement is not None:
        deps=proj_depManagement.find("{%s}dependencies" % ns)
        if deps is not None:
            validDep(deps)

def validPlugin(build_plugins,arg_agent):
    plugins=build_plugins.findall("{%s}plugin" % ns)
    artifactIds=[getArtifactId(plugin) for plugin in plugins]
    
    if "maven-surefire-plugin" not in artifactIds:
        build_plugins.append(buildSureFirePlugin(arg_agent))
    else:
        i=artifactIds.index("maven-surefire-plugin")
        maven_surefire=plugins[i]
        updateSurefirePlugin(maven_surefire,arg_agent)
        
def validPlugins(pom_root,arg_agent):
    build=pom_root.find("{%s}build" % ns) ##project build
    if build is None:
        build=ET.Element("build")
        pom_root.append(build)
        print("new build")
        
    build_plugins=build.find("{%s}plugins" % ns)
    if build_plugins is None:
        build_plugins=ET.Element("plugins")
        build.append(build_plugins)
        print("new build plugin")
    validPlugin(build_plugins,arg_agent)
            
    build_pluginManagement=build.find("{%s}pluginManagement" % ns)
    if build_pluginManagement is not None:
        build_plugins2=build_pluginManagement.find("{%s}plugins" % ns)
        if build_plugins2 is not None:
            validPlugin(build_plugins2,arg_agent)

def mvn_pom(pom_file,proj_name,log): 
    print("check pom_file: ", pom_file, "proj_name: ", proj_name)
    log.info("check pom_file: %s proj_name: %s"%(pom_file,proj_name))
    if not os.path.exists(pom_file+"_original"):
        shutil.copy(pom_file,pom_file+"_original")
        
    pom_root=getPomTree(pom_file)
    jdkversion=getJdkVersion(pom_root)
    ##check dependencies
    validDeps(pom_root)       
    project_profiles=pom_root.find("{%s}profiles" % ns)
    if project_profiles is not None:
        profiles=project_profiles.findall("{%s}profile" % ns)
        for profile in profiles:
            validDeps(profile)
    
    tree=prettify(pom_root)    
    file = open(pom_file, 'w')
    file.write(tree)
    file.close()
    return jdkversion
                        
def agent_pom(pom_file,repo_dir,d,log): ###full name
    print("instrument agent pom_file: ", pom_file, "proj_name: ", repo_dir)
    log.info("instrument agent pom_file: %s proj_name: %s"%(pom_file,repo_dir))
    if not os.path.exists(pom_file+"_mvn"): ##copy pom.xml to pom.xml_mvn
        shutil.copy(pom_file,pom_file+"_mvn")
    
    #global arg_agent
    arg_agent=arg_prefix+repo_dir+"_"+str(d)
    
    pom_root=getPomTree(pom_file)
    ##check plugins
    validPlugins(pom_root,arg_agent)        
    project_profiles=pom_root.find("{%s}profiles" % ns)
    if project_profiles is not None:
        profiles=project_profiles.findall("{%s}profile" % ns)
        for profile in profiles:
            validPlugins(profile,arg_agent)
                    
    tree=prettify(pom_root)    
    file = open(pom_file, 'w')
    file.write(tree)
    file.close()

if __name__== '__main__':
#     if sys.argv is None or len(sys.argv)<2:
#         sys.exit('Error! You need to specify at least one maven project id!!')
    
    pom_file="/home/peipei/RepoReaper/1_4/pom.xml"
    proj="1_4"#/KobisUtils/"#"8_199"
    filename="abc" ##/home/peipei/RepoReaper/RegexCollection/1_bref.csv
    log,fh = createLog("abc.log")
    print(mvn_pom(pom_file,proj,log))
    agent_pom(pom_file, proj, log)
