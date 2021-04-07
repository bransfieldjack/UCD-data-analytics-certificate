
  

# UCD-data-analytics-certificate

  

![](https://exo-demo-image-hosting.s3-ap-southeast-2.amazonaws.com/Screen+Shot+2021-04-07+at+7.13.42+am.png)

  

### Notes

  

How to use this repository? All information in the README.md file is supplementary to the official project report and code. This repository is intended to provide insight into my methods/analysis.

  

<hr>

  

#### Technology used:

  

- python 3.8

  

- conda 4.9.2 (local package/environment management)

  

- VS Code 1.55.0, local text editor. (Pycharm for project delivery but my license expired)

  

- Google collab for quick prototyping

  

- Jupyter notebooks 4.6.3

  

  

#### Packages:

  

- Python requests library for API data retrieval

  

- Pandas for data manipulation

  

- Matplotlib for visualisation

  

  

### Git setup

I am using Mac OS Catalina 10.15.7. 

To get git installed on my local machine, I open the terminal and navigate to my working directory/folder where my project is.
 
```
cd UCD/project/
```
Next I need to initialise this folder with the following command, in order to create a local git repository of my work. (Basically I am telling git to start tracking all of the files/changes in this folder)
```
git init
```
The next thing you will need to do is add a README.md file (this is the file you are reading right now) where you can add notes on packages, setup, how to etc. 
```
git add README.md
```
Next, you need to make your first 'commit'. Commits are like a way of saving your progress as you develop your project. They are instances of your work at a certain point in time, like a save state or snapshot. 
```
git commit -m "first commit"
```
You will also need to specify the name of your 'branch'. Branches are a way of creating multiple different versions of the same code base in the same repository, so that if for example one of your team mates is working on a particular feature that must not yet be integrated with the rest of the code base, this can be achieved using branches.
```
git branch -M main
```  
Next, you need to connect your *local repository* to a *remote repository*. This is optional but recommended, it is also a requisite milestone for the project. Basically you can think of this as being a way of saving your work in a remote location for safe keeping. 
```
git remote add origin https://github.com/bransfieldjack/test.git
```
Finally you can push all of your local changes to the remote:
```
git push -u origin main
```
##### Git cheat sheet:
- ```git init``` initialise your local repo
- ```git status``` show the current status of pending commits/files to be added
- ```git commit -m <message describing commit here>``` making a commit, be sure to add a text description between the <> 
- ```git remote -v``` check which remote repo you are connected to 
- ```git branch``` check which branch you are on
- ```git checkout <new branch>``` create or switch to another branch

Recommended sequential flow for every commit: 
		- ```git status``` (shows your pending changes, usually in red text but depends on your terminal colours)
		- ```git add -A .```
		- ```git status``` (again, will show you all the changes made, usually in green text but depends on your terminal colours)
		- ```git commit -m <add a message here>``` create a commit with a description of what you are committing/the changes you have made.
		- ```git push origin main``` push your local changes to the remote github repository
<hr>

### Some notes about Jupyter Notebooks

  

If you are using jupyter notebooks for the first time you might notice that some of the packages that you are trying to import are not available in the environment...

  

  

![import_error](https://exo-demo-image-hosting.s3-ap-southeast-2.amazonaws.com/Screen+Shot+2021-04-07+at+7.37.11+am.png)

  

To get around this, you can use the pip installer tool in the first cell of the notebook, like this...

  

![jupyter_package_install](https://exo-demo-image-hosting.s3-ap-southeast-2.amazonaws.com/Screen+Shot+2021-04-07+at+7.39.03+am.png)