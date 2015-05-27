import os
rootdir="algae"
#home_dir="/home"
#work_dir="/home/sarunya-w/Documents/Github/CS402-PROJECT/Project/test/"
#ms_dir="/home/sarunya-w/Documents/Github/CS402-PROJECT/Project/test/dataset"
for root, dirs, files in os.walk(rootdir):
	for f in files:
		if f.endswith('jpg') or f.endswith('JPG') or f.endswith('png') or f.endswith('PNG'):
			print os.path.join(root,f)
			inputfile = os.path.join(root,f)
			outputfile = "resized/"+f
			cmd="ffmpeg -i %s -vf scale=1024:-1 %s"%(inputfile,outputfile)
			#cmd="ffmpeg -i %s -vf scale=1024:768 %s"%(inputfile,outputfile)
			os.system(cmd)
  