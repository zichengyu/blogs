## 1 命令帮助

git xxx –help或者man git xxx

git help <command>  # 显示command的help

## 2 设置

设置用户名，

git config --global user.name

设置用户邮箱，

git config --global user.email

设置颜色显示，

git config --global color.ui true

设置提交模板，

git config --global commit.template xxx

## 3 Git初始化

Clone远程版本库：git clone [--bare] <repository> [<directory>]

git clone [git@xbc.me:wordpress.git](mailto:git@xbc.me:wordpress.git)

​    添加远程版本库origin：语法为 git remote add [shortname] [url]  

git remote add origin git@xbc.me:wordpress.git

初始化版本库

Git init 

## 4 显示状态信息

git status -s

## 5 添加提交任务

git add：添加修改文件

git add -i:选择行添加文件

git rm：删除文件

git mv：修改文件名或移动文件

git rm --cached <file>:删除缓存区中的某文件

## 6 显示差异

git diff：比较当前文件和暂存区文件差异

git diff HEAD ：当前版本库与工作区差异

git diff --cached/--stage ：暂存区与版本库差异

## 7 提交修改到本地仓库

git commit：将暂存区任务提交到本地仓库

git commit --amend：修正最后一次提交

## 8 显示提交日志和内容

git log --before=2016.7.16 --after=2016.7.15 --author=yuzicheng：查找时间在20160716和20160715之间的自己的提交日志

git log：只是显示简单的提交记录

git log -p：显示具体的文件修改

git show：# 显示某次提交的内容

git reflog：查看历次提交的版本号

git reflog expire --expire=now --all 清楚所有日志，这样会使reflog全部记录都过期，从而commit、blob、tree对象都会变成未被关联的dangling对象

git log --graph --oneline 显示树形结构，不显示对应的详细信息

git log --graph --pretty=oneline --stat 格式化日志输出，显示树形结构，显示对应的详细信息

## 9 远程操作

git pull : 获取远程更新并合并到本地仓库

git push : 将当前提交推送到远程仓库

## 10分支操作

git branch：显示本地分支

git branch -a：显示本地和远程所有分支

git branch <branch>：创建本地分支

git branch -d <branch>：删除本地分支

git branch -m <branch>：修改本地分支

## 11 重置

git reset -- filename 用commit节点的文件替换暂存区中的文件,不改变引用和工作区，同git reset HEAD filename

git reset --soft <commit>：改变引用指向到commit节点，不改变暂存区和工作区

git reset --mixed <commit>：改变引用指向到commit节点，并且用commit节点内容替换暂存区，不改变工作区

git reset --hard <commit>：改变引用指向到commit节点，并且用commit节点内容替换暂存区和工作区

git reset --hard HEAD^5   git回转到上第几5个版本

## 12 检出

git checkout 汇总显示工作区缓存区和HEAD的差异，同git checkout HEAD

git checkout <branch>：切换到分支branch，实际上就是让.git/HEAD中不是指向.git/refs/heads/master，而是为.git/HEAD指定一个具体的提交ID

git checkout -b <new_branch> [<start_point>]：从start_point创建新分支，并切换到新分支

git checkout -- filename 用缓存区中的文件替换当前工作空间的文件

git checkout branch -- filename 维持HEAD的内容不变，用branch中的该文件直接覆盖缓存区和工作区中的文件

git checkout HEAD ./filename  用master中的文件替换暂存区和工作区中的全部/某文件

git checkout ./filename 用暂存区中的文件替换工作区中的全部/部分文件

## 13 反转提交

git revert <commit>：撤销commit节点的提交

git revert HEAD     # 恢复最后一次提交的状态

## 14 冲突解决

git merge [--no-commit] <commit>：将commit节点内容合并到当前分支

git mergetool：通过工具来合并

## 15 里程碑

git tag -m <msg> <tagname> [<commit>]：在commit节点创建一个名为tagname 的tag，说明信息为msg

## 16 保存Git工作现场

​    git stash save 说明 保存进度的时候同时指定说明

git stash：保存当前工作现场，等以后恢复现场后继续工作

git stash clear 清除所有stash

Git stash branch <branchname> <stash> 基于进度创建分支

恢复以前保存的现场继续工作

### 1、查看列表git stash list

### 2、git stash apply [--list][]恢复

​	恢复后stash并不会删除，--list表示同时尝试恢复缓存区，stash指定的回复哪一个stash

### 3、git stash pop [--list][] 恢复

​	恢复的同时删除stash,--list表示同时尝试恢复缓存区，stash指定的回复哪一个stash

## 17 查看git对象的内容或者对象信息

git cat-file -p HEAD 查看HEAD对象的信息

git cat-file -t HEAD 查看HEAD对象的类型

## 18 删除多余的目录和文件

​    git clean -nd 查看将要删除那些目录和文件

​    git clean -fd 强制删除多余的目录和文件

## 19 文件追溯

git blame filename  

## 20 其他

git prune 清楚未被关联的dangling对象

git fask 查看未被关联到的对象

git repack 对松散对象进行打包

git gc 对版本库进行整理，默认为两周，如果使用--prune=now，则直接就完成对未关联对象的清理

git mergetool 冲突解决工具

git ls-tree -l HEAD 查看HEAD指向的目录树

git rebase -i HEAD~3 从HEAD版本开始往过去数3个版本

git rebase -i hash码 指名要合并的版本之前的版本号（请注意指定的这个版本是不参与合并的，可以把它当做一个坐标）

 