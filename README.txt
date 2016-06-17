-Project Title :
Smart Image Sharing Platform
-By:
Ankit Vadehra, 12BCE0282, <ankit.vadehra2012@vit.ac.in>
Rohan Kumar, 12BCE0622, <rohan.kumar2012@vit.ac.in>
--------------------------------------------------
-Project Installation :
*We require a UNIX/Linux environment to succesfully run the application:

1)Check if "pip" is installed in your system:
~$ pip --version
Should return version or "bash: pip: command not found"
If command not found, install pip:
~$ curl -O http://peak.telecommunity.com/dist/ez_setup.py
~$ sudo python ez_setup.py
~$ sudo easy_install pip

2)Install Virtualenv so that we have an isolated environment for our project.
~$ sudo pip install virtualenv

3)Create a virtualenv and install required modules.
~$ virtualenv ~/Documents/shareit
~$ source ~/Documents/shareit/bin/activate
~$ pip install -r requirements.txt

All this has to be done in a local filesystem. Use the requirements.txt file in the CD.

3)Copy the folder webUI in the local filesystem. For this project we assume you copy the webUI folder in ~/Documents folder.

4)Enter the location of webUI/shareit in:
"webUI/shareit/dirLocation.txt", and, "webUI/CaptionGen/captionGeneration/codes/dirLocation.txt"
*THIS IS IMPORTANT. So the location will be something like "/home/<user>/Documets/webUI/shareit"

5)Start the system by entering:
~$ python /home/<user>/Documets/webUI/shareit/shareit.py
This will start the system at URL: "http://localhost:5000/"

6)Upload some images, post comments, likes and dislikes.

7)Run
~$ python /home/<user>/Documets/webUI/CaptionGen/captionGeneration/codes/submit_captions.py
This will generate captions for your images.

8) Open http://localhost:5000/trending, to see the trending images.

9)Open a site like http://localhost:5000/search?query=dog, to see images tagged with the caption "dog".

10)After finishing the project, close terminal, or enter
~$ deactivate
To move out of virtualenv Python.