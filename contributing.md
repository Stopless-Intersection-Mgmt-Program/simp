# Stopless Intersection Management Contributing

Guide to Contributing to Source Repositories

After our github repository is made it will be necessary to organize the development of features to separate branches.

Clone the remote repository into a local repository on your computer. This can be done by HTTPS or with SSH

    git clone <https or ssh link>

Once inside the local repository, go to our current development branch

    git checkout developmentBranch

create a new branch for your task/feature:

    git checkout -b <your-new-featureBranch>

ideally the name should describe the feature being added. Once your changes have been implemented into the local repository commit them by doing:

    git commit -m “Message about changes”

Once code is implemented and ready to be pushed to the github repository enter the following:

    git push -u origin <your-new-featureBranch>

On the repository you should see a compare & pull request option to submit a pull request (make sure the base branch is the developmentBranch), 
submit and then your done.

-----------------------------------------------------------------------------------------------------------------------------------------------------------

Make sure all files are up to date with the current developmentBranch, always git pull before committing and pushing to development.
