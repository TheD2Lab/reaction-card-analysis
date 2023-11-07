import csv
import copy
from wordcloud import WordCloud
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import numpy as np


# Function for setting color grouping
class SimpleGroupedColorFunc(object):

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


# Heuristic categories
heuristicsList = [

    # H1: Visibility of System Status
    [["Collaborative", "Comprehensive", "Engaging", "Essential"], ["Overwhelming"]],

    # H2: Match Between System & Real World
    [["Comfortable", "Familiar", "Friendly"], ["Confusing"]],

    # H3: User Control & Freedom
    [["Entertaining", "Exciting", "Inspiring", "Satisfying"], ["Impersonal", "Rigid"]],

    # H4: Consistence & Standards
    [["Consistent", "Predictable", "Straight Forward"], ["Inconsistent", "Unconventional", "Unpredictable"]],

    # H5: Error Prevention
    [["Organized", "Trustworthy"], ["Poor quality"]],

    # H6: Recognition Rather Than Recall
    [["Convenient", "Helpful", "Useful"], ["Complex"]],

    # H7: Flexibility & Efficiency of Use
    [["Advanced", "Cutting edge", "Easy to use", "Effective", "Efficient", "Exceptional", "Fast", "Flexible",
      "High quality", "Innovative"], ["Annoying", "Difficult", "Stressful", "Time-consuming"]],

    # H8: Aesthetic & Minimalist Design
    [["Approachable", "Attractive", "Clean", "Creative", "Desirable", "Inviting", "Professional", "Relevant",
      "Simplistic"], ["Busy", "Dated", "Dull", "Intimidating", "Irrelevant", "Unattractive", "Undesirable"]],

    # H9: Recognize, Diagnose, & Recover from Errors
    [["Powerful", "Reliable"], ["Ineffective", "Unrefined"]],
]

# Setting word cloud scope
print("1. Overall Study\n"
      "2. LIL Visualization\n"
      "3. Matrix Visualization\n")

studyType = int(input("1-3: "))
print()

study = ""

if studyType == 1:
    study = "overall"
    partNum = 1

elif studyType == 2:
    study = "lil"
    partNum = 1

elif studyType == 3:
    study = "matrix"
    partNum = 2

# Initializing dictionary & input file
wordFreq = dict()
inputFile = "raw.count." + study + ".csv"

# Reading in word-frequencies from input file
with open(inputFile, mode='r') as reactionFile:
    fileReader = csv.reader(reactionFile, delimiter=',')

    for row in fileReader:
        wordFreq[str(row[0])] = float(row[1])

# All-heuristic word clouds

# Heuristics color palette (Maximum Contrast/USWDS Token Compromise)
heurCol1 = '#ddaa01'  # Yellow 30v
heurCol2 = '#8168b3'  # Violet 50
heurCol3 = '#e66f0e'  # Orange 40v
heurCol4 = '#58b4ff'  # Blue 30v
heurCol5 = '#b21d38'  # Red Cool 60v
heurCol6 = '#c7a97b'  # Gold 30
heurCol7 = '#76766a'  # Gray Warm 50
heurCol8 = '#04c585'  # Mint 30v
heurCol9 = '#ff87b2'  # Magenta 30v

# Setting color groupings
color_to_words = {
    heurCol1: heuristicsList[0][0] + heuristicsList[0][1],
    heurCol2: heuristicsList[1][0] + heuristicsList[1][1],
    heurCol3: heuristicsList[2][0] + heuristicsList[2][1],
    heurCol4: heuristicsList[3][0] + heuristicsList[3][1],
    heurCol5: heuristicsList[4][0] + heuristicsList[4][1],
    heurCol6: heuristicsList[5][0] + heuristicsList[5][1],
    heurCol7: heuristicsList[6][0] + heuristicsList[6][1],
    heurCol8: heuristicsList[7][0] + heuristicsList[7][1],
    heurCol9: heuristicsList[8][0] + heuristicsList[8][1]
}

# Configuring & generating word cloud
default_color = "black"
simple_color_func = SimpleGroupedColorFunc(color_to_words, default_color)

wc = WordCloud(width=1920, height=1080, prefer_horizontal=1,
               background_color="#FFFFFF").generate_from_frequencies(wordFreq)
wc.recolor(color_func=simple_color_func)

plt.xticks([])
plt.yticks([])

# Configuring the font color legend
fontColors = [Patch(facecolor=heurCol1, edgecolor=heurCol1, label='H1: Visibility of System Status'),
              Patch(facecolor=heurCol2, edgecolor=heurCol2, label='H2: Match between System & Real World'),
              Patch(facecolor=heurCol3, edgecolor=heurCol3, label='H3: User Control & Freedom'),
              Patch(facecolor=heurCol4, edgecolor=heurCol4, label='H4: Consistency & Standards'),
              Patch(facecolor=heurCol5, edgecolor=heurCol5, label='H5: Error Prevention'),
              Patch(facecolor=heurCol6, edgecolor=heurCol6, label='H6: Recognition Rather Than Recall'),
              Patch(facecolor=heurCol7, edgecolor=heurCol7, label='H7: Flexibility & Efficiency of Use'),
              Patch(facecolor=heurCol8, edgecolor=heurCol8, label='H8: Aesthetic & Minimalist Design'),
              Patch(facecolor=heurCol9, edgecolor=heurCol9, label='H9: Recognize, Diagnose, & Recover from Errors')]

colorLegend = plt.legend(handles=fontColors, fontsize='x-small', loc='upper left', bbox_to_anchor=(1, 1))
plt.gca().add_artist(colorLegend)

# Generating list of corresponding word frequencies & font sizes
freqSizes = []
for layout in wc.layout_:
    freqSizes.append((int(wordFreq[str(layout[0][0])]), layout[1]))

# Removing duplicates, Sorting freqSize list by font size
freqSizes = list(set(freqSizes))
freqSizes.sort(key=lambda x: x[1])

# Splitting freqSize list into 5 frequency/size ranges
freqSizesArray = np.array(freqSizes)
freqSizeSplits = np.array_split(freqSizesArray, 5)

# Configuring font size legend (27 spaces to match font color legend boundary)
fontSizes = [Patch(color='none', label=f"{'Font Size:':<18} {'Word Freq:' :>18}          ")]

for freqSizeList in freqSizeSplits:
    sizeRange = f"[{str(freqSizeList[0][1]).zfill(3)}-{str(freqSizeList[-1][1]).zfill(3)}]"
    freqRange = f"[{str(freqSizeList[0][0]).zfill(3)}-{str(freqSizeList[-1][0]).zfill(3)}]"

    fontSizes.append(Patch(color='none', label=f"{sizeRange:<8}{' →':^16}{freqRange:>8}"))

sizeLegend = plt.legend(handles=fontSizes, fontsize='x-small', loc='upper left', bbox_to_anchor=(1, 0.50))
plt.gca().add_artist(sizeLegend)

# Saving word cloud + legends as a .png file
plt.imshow(wc)
plt.savefig(study.capitalize() + " Word Cloud (All Heuristics).png",
            dpi=300, bbox_extra_artists=[colorLegend], bbox_inches='tight')

# Per-heuristic word clouds
fig, axs = plt.subplots(3, 3)
plt.rcParams['axes.titlesize'] = 'medium'

posColor = "#276CBD"  # blue 50v
negColor = "#D51C3C"  # red 50v

fontSizes = [Patch(color='none', label='Heuristic Legend'),
             Patch(color='none', label='[Font Size]  → [Word Freq]')]

# Generating each individual word cloud
for i in range(9):

    # Isolating words by heuristic group
    wordFreqCopy = copy.deepcopy(wordFreq)
    for word in wordFreq.keys():
        if word not in (heuristicsList[i][0] + heuristicsList[i][1]):
            del wordFreqCopy[word]

    # Configuring individual word cloud
    color_to_words = {
        posColor: heuristicsList[i][0],
        negColor: heuristicsList[i][1]
    }

    default_color = "black"
    simple_color_func = SimpleGroupedColorFunc(color_to_words, default_color)

    wc = WordCloud(width=1920, height=1080, prefer_horizontal=1,  # relative_scaling=1,
                   background_color="#FFFFFF").generate_from_frequencies(wordFreqCopy)
    wc.recolor(color_func=simple_color_func)

    # Generating list of corresponding word frequencies & font sizes
    freqSizes = []

    for layout in wc.layout_:
        freqSizes.append((int(wordFreq[str(layout[0][0])]), layout[1]))

    # Removing duplicates, Sorting freqSize list by font size
    freqSizes = list(set(freqSizes))
    freqSizes.sort(key=lambda x: x[1])

    # Splitting freqSize list into 1/3 frequency/size ranges
    freqSizesArray = np.array(freqSizes)

    if (i == 6) or (i == 7):
        freqSizeSplits = np.array_split(freqSizesArray, 3)
    else:
        freqSizeSplits = np.array_split(freqSizesArray, 1)

    # Appending individual word cloud info to font size legend
    fontSizes.append(Patch(color='none', label=''))
    fontSizes.append(Patch(color='none', label=f"Heuristic #{i+1}"))

    for freqSizeList in freqSizeSplits:
        sizeRange = f"[{str(freqSizeList[0][1]).zfill(3)}-{str(freqSizeList[-1][1]).zfill(3)}]"
        freqRange = f"[{str(freqSizeList[0][0]).zfill(3)}-{str(freqSizeList[-1][0]).zfill(3)}]"

        fontSizes.append(Patch(color='none', label=f"{sizeRange}   →   {freqRange}"))

    sizeLegend = plt.legend(handles=fontSizes, fontsize='xx-small', loc='upper left', bbox_to_anchor=(1.095, 4.225))
    plt.gca().add_artist(sizeLegend)

    # Setting word cloud title based on heuristic
    if i < 3:
        x = 0
    elif i < 6:
        x = 1
    else:
        x = 2

    y = i % 3

    axs[x, y].imshow(wc)

    if i == 0:
        axs[x, y].set_title("H1: Visibility of\nSystem Status", pad=9)
        # fontSizes.append(Patch(color='none', label=f"Heuristic #1: Visibility..."))
    elif i == 1:
        axs[x, y].set_title("H2: Match between\nSystem & Real World", pad=9)
        # fontSizes.append(Patch(color='none', label=f"Heuristic #2: Match..."))
    elif i == 2:
        axs[x, y].set_title("H3: User Control\n& Freedom", pad=9)
        # fontSizes.append(Patch(color='none', label=f"Heuristic #3: User..."))
    elif i == 3:
        axs[x, y].set_title("H4: Consistency\n& Standards", pad=9)
        # fontSizes.append(Patch(color='none', label=f"Heuristic #4: Consistency..."))
    elif i == 4:
        axs[x, y].set_title("H5: Error\nPrevention", pad=9)
        # fontSizes.append(Patch(color='none', label=f"Heuristic #5: Error..."))
    elif i == 5:
        axs[x, y].set_title("H6: Recognition\nRather Than Recall", pad=9)
        # fontSizes.append(Patch(color='none', label=f"Heuristic #6: Recognition..."))
    elif i == 6:
        axs[x, y].set_title("H7: Flexibility &\nEfficiency of Use", pad=9)
        # fontSizes.append(Patch(color='none', label=f"Heuristic #7: Flexibility..."))
    elif i == 7:
        axs[x, y].set_title("H8: Aesthetic &\nMinimalist Design", pad=9)
        # fontSizes.append(Patch(color='none', label=f"Heuristic #8: Aesthetic..."))
    elif i == 8:
        axs[x, y].set_title("H9: Recognize, Diagnose,\n& Recover from Errors", pad=9)
        # fontSizes.append(Patch(color='none', label=f"Heuristic #9: Recognize..."))

# Removing all tick-marks from word cloud matrix
for ax in axs.flat:
    ax.set_xticks([])
    ax.set_yticks([])

# Configuring the font color legend
fontColors = [Patch(facecolor=posColor, edgecolor=posColor, label='Positive Words                '),
              Patch(facecolor=negColor, edgecolor=negColor, label='Negative Words                ')]

colorLegend = fig.legend(handles=fontColors, fontsize='xx-small', loc='upper left', bbox_to_anchor=(1, 1))
plt.gca().add_artist(colorLegend)

# Formatting & saving the word cloud matrix
plt.tight_layout(w_pad=1.5, h_pad=3)
plt.savefig(study.capitalize() + " Word Clouds (Per Heuristic).png",
            dpi=300, bbox_extra_artists=[colorLegend], bbox_inches='tight')
