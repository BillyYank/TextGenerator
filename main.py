import statistics_maker
import textGen
import sys

if sys.argv[1] == "make_stat":
    statistics_maker.StatMaker(sys.argv[2]).make_stat()
elif sys.argv[1] == "gen_text":
    text_generator = textGen.TextGenerator("text")
    text_generator.load_stat("statistics.json")
    text_generator.save_text(int(sys.argv[2]))

