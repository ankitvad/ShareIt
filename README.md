# ShareIt
Smart image sharing platform with Nudity detection using image processing and Image caption generation and similarity ranking using Deep Learning.
<hr><br>
<h3>Project Installation</h3>
<ol>
<li>Check if "pip" is installed in your system
<pre><code>~$ pip --version</code></pre>
Should return version or <code>"bash: pip: command not found"</code><br>
If command not found, install pip:<pre><code>
~$ curl -O https://bootstrap.pypa.io/get-pip.py
~$ sudo python get-pip.py
</code></pre></li>
<li>Install Virtualenv so that we have an isolated environment for our project.
<pre><code>~$ sudo pip install virtualenv</code></pre></li>
<li>Create Virtualenv and install required modules.
<pre><code>
~$ virtualenv ~/Documents/shareit
~$ source ~/Documents/shareit/bin/activate
~$ pip install -r requirements.txt
</code></pre>
All this has to be done in a local filesystem. Use the requirements.txt file in the repository.</li>
<li>Copy the folder webUI in the local filesystem. For this project we assume you copy the webUI folder in ~/Documents folder.</li>
<li>
Enter the location of shareit in <code>webUI/shareit/dirLocation.txt"</code>.<br>
*THIS IS IMPORTANT. So the location will be something like <code>"/home/USER_NAME/Documets/shareit"</code></li>.
<li>
Start the system by entering:<br>
<code>~$ python /home/USER_NAME/Documets/ShareIt/shareit.py</code><br>
This will start the system at URL: <code>"http://localhost:5000/"</code>.
<li> Caption Generation using Deep Learning is done using Python's Chainer library and inspiration was taken by this project: <a href="https://github.com/dsanno/chainer-image-caption">chainer-image-caption</a> by @dsanno. After setting it up, a simple CRON job was initiated that enters the captions in the SQLite database. Modifications were made to the project to achieve this. Please open an issue, or shoot me an email, if you siwh to know how I set up this step.</li>
<li>
Open <code>http://localhost:5000/trending</code>, to see the trending images. We have used the lower bound of Wilsons Interval on the Likes and Dislikes aggregated on each image. This is the method used by Reddit to achieve the same functionality. More information on the maths and logic can be gathered from here:<br>
<a href="http://www.evanmiller.org/how-not-to-sort-by-average-rating.html">Evan Millers Blog</a><br>
<a href="https://medium.com/hacking-and-gonzo/how-reddit-ranking-algorithms-work-ef111e33d0d9#.cqd7ct6km">Medium-Blog Post</a>
</li>
<li>
Open a site like <code>http://localhost:5000/search?query=dog</code>, to see images tagged with the caption "dog". This can only be done after Caption Generation has been run once or more.</li>
<li>
After finishing the project, close terminal, or enter <code>~$ deactivate</code>, To move out of virtualenv Python.</li>
</ol>
<hr><br>
Profanity detection happens using 2 distinct image processing algorithms whenever the user tries to upload a new image in the system.
<br>
License: Standard MIT License.<br>
For more infomation, please check:<br>
<ul> 
<li>Brief Information - <a href="presentaion.pdf">Presentation</a></li>
<li>Detailed Literature - <a href="doc_details.pdf">Document</a>
<hr>