#!/usr/bin/python

from core import goingson, music, politics, art

# Main Function
def main():

	# Initilaize Goings On File
	goingson.printSection('start')
	goingsonsf = []

	# Politics
	goingson.printSection('Politics')
	goingsonsf.append(politics.Commonwealth().toDF())
	goingsonsf.append(politics.WorldAffairsCouncil().toDF())

	# Music
	goingson.printSection('Music')
	goingsonsf.append(music.Fillmore().toDF())
	goingsonsf.append(music.APE().toDF())
	goingsonsf.append(music.SFSymphony().toDF())

	# Art
	goingson.printSection('Art')
	goingsonsf.append(art.SFMoMA().toDF())

	# Combine and Output Results
	goingsonsf = goingson.combine_results(goingsonsf)
	goingson.outputResults(goingson_df=goingsonsf)
	goingson.printSection('end')


if __name__ == '__main__':
	main()