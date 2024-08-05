# git使用

整理自廖雪峰 

https://www.liaoxuefeng.com/wiki/896043488029600/896827951938304

```
# 创建仓库
git init

# 把文件添加到仓库
git add readme.txt

# 文件提交到仓库
# git commit命令，-m后面输入的是本次提交的说明，可以输入任意内容
git commit -m "wrote a readme file"

# 仓库当前的状态
git status

# 查看修改内容
git diff readme.txt

# 查看git提交log
# head 表示当前版本
# head^ 表示上一个版本
# head~100 表示前100个版本
git log --pretty=oneline

# 回退版本
# 回退到上一个版本
git reset --hard HEAD^
# 恢复原来版本
git reset --hard commit id

# 命令记录
git reflog

```

第一步是用`git add`把文件添加进去，实际上就是把文件修改添加到暂存区 stage；

第二步是用`git commit`提交更改，实际上就是把暂存区的所有内容提交到当前分支。



场景1：当你改乱了工作区某个文件的内容，想直接丢弃工作区的修改时，用命令`git checkout -- file`。

场景2：当你不但改乱了工作区某个文件的内容，还添加到了暂存区时，想丢弃修改，分两步，第一步用命令`git reset HEAD <file>`，就回到了场景1，第二步按场景1操作。

场景3：已经提交了不合适的修改到版本库时，想要撤销本次提交，参考[版本回退](https://www.liaoxuefeng.com/wiki/896043488029600/897013573512192)一节，不过前提是没有推送到远程库。

```
# 撤销修改
# 命令git checkout -- readme.txt意思就是，把readme.txt文件在工作区的修改全部撤销，这里有两种情况：
# 一种是readme.txt自修改后还没有被放到暂存区，现在，撤销修改就回到和版本库一模一样的状态；
# 一种是readme.txt已经添加到暂存区后，又作了修改，现在，撤销修改就回到添加到暂存区后的状态。
# 总之，就是让这个文件回到最近一次git commit或git add时的状态。
git checkout -- readme.txt

# 撤销进入stage的修改
git reset HEAD readme.txt
git restore --staged readme.txt

# 丢弃工作区的修改
git checkout -- readme.txt
```

将文件提交到版本库后，删除这个文件

```
# git add test.txt
# git commit -m "add test.txt"

# 工作区删除 rm test.txt

# 情况一
# 删除版本库中的文件
git rm test.txt
git commit -m "remove test.txt"

# 情况二
# 误删除，需要恢复工作区中的文件
# git checkout其实是用版本库里的版本替换工作区的版本，无论工作区是修改还是删除，都可以“一键还原”。
# 只能恢复文件到最新版本，你会丢失最近一次提交后你修改的内容。
git checkout -- test.txt

```



# 远程仓库

## ssh加密&添加远程仓库

https://www.liaoxuefeng.com/wiki/896043488029600/896954117292416

https://www.liaoxuefeng.com/wiki/896043488029600/898732864121440

要关联一个远程库，使用命令`git remote add origin git@server-name:path/repo-name.git`；

关联一个远程库时必须给远程库指定一个名字，`origin`是默认习惯命名；

关联后，使用命令`git push -u origin master`第一次推送master分支的所有内容；

此后，每次本地提交后，只要有必要，就可以使用命令`git push origin master`推送最新修改；

```
#  push an existing repository from the command line
git remote add origin git@github.com:SteveLi-0/how_to_use_git.git
git branch -M main
git push -u origin main

git push origin master

```

push到远程仓库时，如果本地master不是基于最新版本修改，需要pull下来merge在push

常见于修改了网页端的readme，导致push不上去，具体解决方法见后文。

# 分支管理

每次提交，Git都把它们串成一条时间线，这条时间线就是一个分支。截止到目前，只有一条时间线，在Git里，这个分支叫主分支，即`master`分支。`HEAD`严格来说不是指向提交，而是指向`master`，`master`才是指向提交的，所以，`HEAD`指向的就是当前分支。

```
# 创建dev分支，然后切换到dev分支
git checkout -b dev
# git checkout -b dev 等价于
git branch dev
git checkout dev

# 查看当前分支
git branch

# 创建分支
git branch <name>

# 切换分支
git checkout <name> 
git switch <name>

# 创建+切换分支
git checkout -b <name>
git switch -c <name>

# 合并某分支到当前分支
git merge <name>

# 删除分支
git branch -d <name>

```

# 冲突

存在冲突的条件是需要待合并的两个分支在分开后同一文件各自有提交

# 分支管理

在不同branch merge的时候，如果是默认fast forward的模式，将看不过开发的dev分支。

可以手动指定no ff模式，合并之后可以保留不同分支合并的历史记录。

```
git merge --no-ff -m "merge with no-ff" dev

git log --graph --pretty=oneline --abbrev-commit
*   e1e9c68 (HEAD -> master) merge with no-ff
|\  
| * f52c633 (dev) add merge
|/  
*   cf810e4 conflict fixed
...
```

# bug分支 & stash & cherry-pick

新功能

- stash
- cherry-pick

当拉出bug分支，但是本地dev分支没法提交时，可以使用stash暂存。

```
# 无论工作区的内容是否提交到暂存区，stash都可以暂时保存
# stash后的工作区是干净的
git stash

# 列出stash内容
git stash list
# stash@{0}: WIP on dev: f52c633 add merge

# 恢复
# pop 恢复的同时把stash内容也删了
git stash pop

# apply 恢复后，stash内容并不删除
git stash apply stash@{0}
```

修复bug的过程，注意此时提交修改bug的id是**4c805e2**

```
git checkout master
git checkout -b issue-101
# fix bug
git add .
git commit -m 'fix bug 101'

[issue-101 4c805e2] fix bug 101
 1 file changed, 1 insertion(+), 1 deletion(-)
 
git switch master
git merge --no-ff -m 'merge fix bug 101' issue-101
```

切换回开发分支dev

```
git switch dev
git stash list
git stash pop
```

master存在的bug，dev上可能也存在。如果不手动修改dev分支上的对应内容，需要cherry-pick 复制一个特定的提交到当前分支。

修复bug的提交是 **4c805e2**  所以只需要在dev上应用一次  **4c805e2** 的修改就可以了。

cherry-pick自动为dev提交一次，提交了dev分支上的bug修改。

```
$ git branch
* dev
  master
$ git cherry-pick 4c805e2
[master 1d4b803] fix bug 101
 1 file changed, 1 insertion(+), 1 deletion(-)
```

# 多人协作

多人协作的工作模式通常是这样：

1. 首先，可以试图用`git push origin <branch-name>`推送自己的修改；
2. 如果推送失败，则因为远程分支比你的本地更新，需要先用`git pull`试图合并；
3. 如果合并有冲突，则解决冲突，并在本地提交；
4. 没有冲突或者解决掉冲突后，再用`git push origin <branch-name>`推送就能成功！

如果`git pull`提示`no tracking information`，则说明本地分支和远程分支的链接关系没有创建，用命令`git branch --set-upstream-to <branch-name> origin/<branch-name>`。

- 查看远程库信息，使用`git remote -v`；
- 本地新建的分支如果不推送到远程，对其他人就是不可见的；
- 从本地推送分支，使用`git push origin branch-name`，如果推送失败，先用`git pull`抓取远程的新提交；
- 在本地创建和远程分支对应的分支，使用`git checkout -b branch-name origin/branch-name`，本地和远程分支的名称最好一致；origin/branch-name 是远程仓库中已经存在的分支。
- 建立本地分支和远程分支的关联，使用`git branch --set-upstream branch-name origin/branch-name`；
- 从远程抓取分支，使用`git pull`，如果有冲突，要先处理冲突。

# rebase

- rebase操作可以把本地未push的分叉提交历史整理成直线；
- rebase的目的是使得我们在查看历史提交的变化时更容易，因为分叉的提交需要三方对比。

# workflow
git checkout cnoa-develop
切换到 cnoa-develop 分支。

git pull
从远程仓库拉取最新的更改并合并到当前分支。

git branch
列出所有本地分支。

git checkout lowsoc-control-dev-v2
切换到 lowsoc-control-dev-v2 分支。

git checkout -b push-use
基于当前分支创建并切换到一个新分支 push-use。

git branch
再次列出所有本地分支，确认新分支的创建和切换。

git rebase cnoa-develop
将当前分支上的提交应用到 cnoa-develop 分支的最新提交之后。

git log
显示当前分支的提交历史。

git push gerrit HEAD:refs/for/cnoa-develop
将当前分支的更改推送到远程仓库的 cnoa-develop 分支，使用 Gerrit 进行代码评审。

git log
再次查看提交历史。

git commit -s --amend
修改最后一次提交，并添加签名。

git push gerrit HEAD:refs/for/cnoa-develop
再次将更改推送到远程仓库的 cnoa-develop 分支。

git branch
再次列出所有本地分支，确认提交后的分支状态。
