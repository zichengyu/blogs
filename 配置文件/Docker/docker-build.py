import os
import argparse
import yaml
import sys

# 本脚本版本号
SCRIPT_VERSION = '1.0'
SCRIPT_RELEASE_DATE = '2018.07.09'

# 本地docker仓库域名
LOCAL_REGISTRY_HOST = 'docker-registry.localhost.com'

# 阿里云docker仓库
ALIYUN_REGISTRY_HOST = 'registry.cn-hangzhou.aliyuncs.com'


def __getPrivateImageNameList(dockerComposeFilePath):
    with open(dockerComposeFilePath, 'r', -1, 'utf-8') as file:
        dcContent = yaml.load(file.read())
    if len(dcContent) == 0:
        return []

    imageList = []
    if 'services' not in dcContent.keys():
        return imageList

    services = dcContent.get('services')
    for key in services.keys():
        service = services.get(key)
        image = service.get('image')
        if len(image) > 0 and image.find(LOCAL_REGISTRY_HOST) == 0:
            imageList.append(image)
    return imageList


def __executeCmdInWorkDir(workDirPath, cmd):
    if len(cmd) == 0:
        print('cmd is empty')
        return False

    if not os.path.exists(workDirPath):
        print('the path of the work dir is not existed')
        return False

    curDir = os.getcwd()

    # change dir
    os.chdir(workDirPath)

    # start app
    status = os.system(cmd)

    # backup dir
    os.chdir(curDir)

    return status == 0


if __name__ == '__main__':
    currentScriptDir = sys.path[0]

    parser = argparse.ArgumentParser(prog='docker-build', description='docker build script')
    parser.add_argument('-b', '--build', dest='command',
                        action='store_const',
                        const='build',
                        default='help',
                        help='build all docker image defined in docker-compose.yml file')

    parser.add_argument('-p', '--push', dest='command',
                        action='store_const',
                        const='push',
                        default='help',
                        help='push all images to local docker registry')

    parser.add_argument('-rm', '--remove', dest='command',
                        action='store_const',
                        const='remove',
                        default='help',
                        help='remove images from local machine which define in docker-compose file(include aliyun tag)')

    parser.add_argument('-pa', '--push-aliyun', dest='command',
                        action='store_const',
                        const='push-aliyun',
                        default='help',
                        help='tag and push all images to aliyun privacy docker registry. You need login first')

    parser.add_argument('-v', '--version', dest='command',
                        action='store_const',
                        const='version',
                        default='help',
                        help='show script version')

    args = parser.parse_args()

    dockerComposeFilePath = os.path.join(currentScriptDir, 'docker-compose.yml')
    dockerImageList = []
    if args.command == 'help' or args.command == 'version':
        pass
    else:
        # check file exited
        if not os.path.exists(dockerComposeFilePath):
            print('docker-compose.yml file not found')
            exit(1)
        dockerImageList = __getPrivateImageNameList(dockerComposeFilePath)
        if len(dockerImageList) == 0:
            print('no any images defined in docker-compose file')
            exit(1)

    if 'help' == args.command:
        print(parser.parse_args(['-h']))

    elif args.command == 'build':
        # step-1
        # clean project
        print('begin to clean project')
        if not __executeCmdInWorkDir(currentScriptDir, 'mvn clean'):
            print('clean project failed!')
            exit(1)
        else:
            print('clean project done')

        # step-2
        # build project
        print('begin to build project')
        if not __executeCmdInWorkDir(currentScriptDir, 'mvn package -Dmaven.test.skip=true'):
            print('build project failed!')
            exit(1)
        else:
            print('build project done')

        # step-2.5
        # save git log into file, so can be pack into images
        gitLogScript = os.path.join(currentScriptDir, 'git-log.py')
        if os.path.exists(gitLogScript):
            __executeCmdInWorkDir(currentScriptDir, 'python git-log.py')

        # step-3
        # build docker images
        print('begin to build docker images')
        if not __executeCmdInWorkDir(currentScriptDir, 'docker-compose build'):
            print('build docker images failed!')
            exit(1)
        else:
            print('---------------------------------------------')
            print('build docker images done. check images fellow:')
            for image in dockerImageList:
                print(image)

    elif args.command == 'remove':
        confirm = input("Are you sure to remove all docker images? (y/n): ")
        if confirm.lower() != 'y':
            print('abort')
            exit(0)
        print('\nbegin to remove docker images from local machine\n')
        aliDockerImageList = []
        for image in dockerImageList:
            aliDockerImageList.append(image.replace(LOCAL_REGISTRY_HOST, ALIYUN_REGISTRY_HOST))
            print("REMOVED: " + image)
            if __executeCmdInWorkDir(currentScriptDir, 'docker rmi ' + image):
                print('done')
            print('')

        # aliyun tag images
        for image in aliDockerImageList:
            print("REMOVED: " + image)
            if __executeCmdInWorkDir(currentScriptDir, 'docker rmi ' + image):
                print('done')
            print('')

        print('remove image done')

    elif args.command == 'push':
        print('begin to push docker images into local registry\n')
        for image in dockerImageList:
            print("PUSH: " + image)
            if __executeCmdInWorkDir(currentScriptDir, 'docker push ' + image):
                print('done')
            print('')

    elif args.command == 'push-aliyun':
        print('begin to push docker images into aliyun registry\n')
        aliImageList = []
        for image in dockerImageList:
            aliImage = image.replace(LOCAL_REGISTRY_HOST, ALIYUN_REGISTRY_HOST)
            aliImageList.append(aliImage)
            print("MAKE TAG: " + aliImage)
            if not __executeCmdInWorkDir(currentScriptDir, 'docker tag  ' + image + ' ' + aliImage):
                print('Failed')

        for image in aliImageList:
            print("PUSH: " + image)
            if __executeCmdInWorkDir(currentScriptDir, 'docker push ' + image):
                print('done')
            print('')

    elif args.command == 'version':
        print("version: " + SCRIPT_VERSION + ' release at ' + SCRIPT_RELEASE_DATE + '\ncreated by liangfen')
    else:
        print(parser.parse_args(['-h']))
