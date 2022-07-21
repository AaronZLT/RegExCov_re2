import subprocess
import re

time1=3600 ##60min
time2=7200 ##120min

def cleanUp(subp):
    # clean up
    if subp.stdin:
        subp.stdin.close()
    if subp.stdout:
        subp.stdout.close()
    if subp.stderr:
        subp.stderr.close()


def calRegex(repo_dir,m,log):
    p1=subprocess.Popen(["grep","-nr",m,repo_dir],stdout=subprocess.PIPE)
    p2=subprocess.Popen(["wc","-l"],stdin=p1.stdout,stdout=subprocess.PIPE) ##example of piped command line
    p1.stdout.close()
    p1.wait()
    output,err=p2.communicate()
    p2.stdout.close()
    p2.wait()

    output_regex=output.strip().decode('utf-8')
    log.info("java.util.regex output: %s" % output)
    if err:
        log.error("java.util.regex error: %s" % err)
    ret=p2.returncode
    if ret>0:
        log.info("java.util.regex ret code: %d" % ret)
    return int(output_regex),err

def isMaven(repo_dir,log):
    p_pom=subprocess.Popen(["find",repo_dir,"-name","pom.xml"],stdout=subprocess.PIPE)
    p_pom_xml=subprocess.Popen(["wc","-l"],stdin=p_pom.stdout,stdout=subprocess.PIPE) ##example of piped command line find|wc
    p_pom.wait()
    output_xml,err_xml=p_pom_xml.communicate()
    p_pom_xml.wait()

    output_xml=output_xml.strip().decode('utf-8')
    log.info("pom.xml output| total number of pom.xml: %s" % output_xml)
    if err_xml:
        log.error("pom.xml error: %s" % err_xml)
    ret=p_pom_xml.returncode
    if ret>0:
        log.info("pom.xml ret code: %d" % ret)
    return int(output_xml),err_xml

def sortPom(log):
    p_pom2=subprocess.Popen(["find",".","-name","pom.xml","-printf","%d:%h\n"],stdout=subprocess.PIPE)
    p_pom_sort=subprocess.Popen(["sort","-n"],stdin=p_pom2.stdout,stdout=subprocess.PIPE) ##example of piped command line find|sort by depth
    p_pom2.wait()
    output_sort,err_sort=p_pom_sort.communicate()
    p_pom_sort.wait()

    output_sorts=re.split(b":|\n",output_sort.strip())
    log.info("pom sort output strip: %s" % output_sorts)
    if err_sort:
        log.info("pom sort error: %s" % err_sort)
    return output_sorts,err_sort


def compileRepo(repo_dir,pom_dir,log,timelog):
    log.info("find pom.xml at the project: %s directory: %s"%(repo_dir,pom_dir))
    print("mvn compile find pom.xml at the project: ",repo_dir," directory: ",pom_dir)
    log.info("now run mvn compile")
    print("now run mvn compile")
    try:
        p_mvn_compile=subprocess.Popen(["mvn","compile"],stdout=subprocess.PIPE)
        output,err=p_mvn_compile.communicate(timeout=time1)

        cleanUp(p_mvn_compile)
        p_mvn_compile.wait()

        if err:
            output_mvn_compile=output.strip().decode('utf-8','replace')
            log.info("mvn compile repo: %s output: %s" % (repo_dir,output_mvn_compile))
            log.error("mvn compile repo: %s error: %s" % repo_dir,err)
        ret=p_mvn_compile.returncode
        
        if ret>0:
            output_mvn_compile=output.strip().decode('utf-8','replace')
            log.info("mvn compile error repo: %s output: %s" % (repo_dir,output_mvn_compile))
            return False
        log.info("mvn compile success repo:%s"%repo_dir)
        return True
    except subprocess.TimeoutExpired:
        log.info("mvn compile time out")
        print("mvn compile time out")
        cleanUp(p_mvn_compile)
        p_mvn_compile.kill()
        timelog.info("mvn compile Exception time out repo: %s"%repo_dir)
        ret=1 ##error status code
    
    return False   
    

def testRepo(repo_dir,log,timelog):
    log.info("now run mvn test")
    print("now run mvn test")       
    try:
        p_mvn_test=subprocess.Popen(["mvn","test"],stdout=subprocess.PIPE)
        output,err=p_mvn_test.communicate(timeout=time1)
        
        cleanUp(p_mvn_test)
        ret=p_mvn_test.wait()
        ret=p_mvn_test.wait()
        p_mvn_test.stdout.close()
        if err:
            output_mvn_test=output.strip().decode('utf-8','replace')
            log.info("mvn test repo: %s output: %s" % (repo_dir,output_mvn_test))
            log.error("mvn test error: %s" % err)       
        ret=p_mvn_test.returncode
        
        if ret>0:
            output_mvn_test=output.strip().decode('utf-8','replace')
            log.info("mvn test error repo: %s output: %s" % (repo_dir,output_mvn_test))
            return False
        log.info("mvn test success repo:%s"%repo_dir)
        return True
    except subprocess.TimeoutExpired:
        log.info("mvn test time out")
        print("mvn test time out")
        cleanUp(p_mvn_test)
        p_mvn_test.kill()        
        timelog.info("mvn test Exception time out repo: %s"%repo_dir)
        ret=1
    
    return False    
    
