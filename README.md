# simp

Guide to Contributing to Source Repositories

After our github repository is made it will be necessary to organize the development of features to separate branches.

Clone the remote repository into a local repository on your computer.
This can be done by HTTPS or with SSH

1. git clone <https or ssh link from github>
  
Once inside the local repository,
go to our current development branch
  
2. git checkout developmentBranch

create a new branch for your task/feature:
  
3. git checkout -b <name-of-new-branch>
  
ideally the name should describe the feature being added.
Once your changes have been implemented into the local repository commit them by doing:
  
4. git commit -m “Message about changes”
  
Once code is implemented and ready to be pushed to the github repository enter the following:
  
5. git push -u origin <your new branch>
  
On the repository you should see a compare & pull request option to submit a pull request (make sure the base branch is the developmentBranch),
submit and then your done.
