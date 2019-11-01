
#Import things
import random
import pandas as pd
from matplotlib import pyplot as plt

'''
My First Python programme

Goal: Replicate the Weasel Programme from Dawkins The Blind Watchmaker.

Function: Dawkins shows that random mutation AND selection can quickly select for a desired trait to mimic evolution

It is applying evolutionary theory to the question of how long a room of monkeys with typewriters would take to come
up with a Shakespeare play.

We have a target sequence from Hamlet, 'METHINKS IT IS LIKE A WEASEL', and the goal is to create a string of random
letters of the same length as the target, copy that string 100 times (it has 100 children) and have a 5% chance of any
letter in the string mutating to a random new letter. We then select the child that is most similar to the target
sequence and then repeat the process with 100 grand children of the original random parent string. This process is
repeated until we arrive at the target sequence.

Without the selection step every generation there is 27^28 (or ~10^40) chance of a monkey typing the phrase on a
typewriter.

With selection after every generation we cam get from a random string to the target sequence in around 100 generations.

'''


###

# check how similar string is to the original

###

def hamdist(str1, str2):
    same = 0
    for chr1, chr2 in zip(str1, str2):
        if chr1 == chr2:
            same += 1
    return same

###

#Weasel Function

###

def data_weasel(target_input, n_offspring, mutate_rate):
    target = list(target_input) #convert target strong to a list
    input_len = len(target) #length of string being used
    #print('inputs')
    #print(target_input)
    #print(input_len)
    #n_offspring = 100 # now an input
    #mutate_rate = 0.05 # now an input
    best_hit = []   #Empty list for a rolling best hit during selection within a generation
    best_hit_each_generation = []   #best hit from the generation (this could be the original best hit)
    best_baseline = float("-inf") #this could go down, start at negative infinity
    gen = 0 # counter, starts at 0


    #generate random string of length target
    parent = [] #a random strong of the same length as the target
    for i in range(len(target)):
        parent.append(random.choice(alphabet)) #using the alphabet variable

    original_parent = parent #want to save the original random input string for later
    #mutate and evolve
    while target != best_hit and gen < 1000:
        gen = gen + 1

        #create n_offspring children with each loci having a mutate_rate chance of mutating to any letter, including itself
        child_list = []

        for i in range(n_offspring):

            child=[]
            for letter in parent:

                chance = random.random()
                if chance > mutate_rate:
                    child.append(letter)

                else:
                    new_letter = random.choice(alphabet)
                    child.append(new_letter)

            child_list.append(child)
        #print(child_list)



        #I have n_offspring mutated children in child_list, need to run through them to find the best hit to the target sequence
        baseline = float("-inf") # could go down
        for kid in child_list:
            #print(kid)
            same = hamdist(kid, target)
            #print(same)
            #print(kid)
            if same > baseline:
                baseline = same
                best_hit = kid
                #print(baseline)
                #print(best_hit)
        best_hit_each_generation.append([gen, best_hit,baseline])

        parent = best_hit
        best_baseline = baseline






    weasel_out={}
    weasel_out = {'target' : ''.join(target),
                  'original_parent' : ''.join(original_parent),
                  'parent' : ''.join(parent),
                  'input_len' : int(input_len),
                  'n_offspring' : int(n_offspring),
                  'mutate_rate' : float(mutate_rate),
                  'gen' : int(gen),
                  'best_baseline' : int(best_baseline)}


    #useful outputs
    return weasel_out


#function is now working.

''' 
I want to optimize the mutation rate, I will run the data weasel function with the original strings, and then identify 
the best mutation rate from the original log series, and then rerun the function with 5 mutation rates spaced between 
the mutation rate either side of the mean. 

And repeat this 10 times to reach an optimal rate

'''

#set up values and variables
#target_list = ['METHINKS IT IS LIKE A WEASEL', 'ALAS POOR YORICK I KNEW HIM HORATIO A FELLOW OF INFINITE JEST OF MOST EXCELLENT FANCY', 'AND GENTLEMEN IN ENGLAND NO ABED SHALL THINK THEMSELVES ACCURSED THEY WERE NOT HERE AND HOLD THEIR MANHOODS CHEAP WHILES ANY SPEAKS THAT FOUGHT WITH US UPON SAINT CRISPINS DAY'] # and this is why there is a limit on the number of generations
target_list = ['METHINKS IT IS LIKE A WEASEL']
 # now an input

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ " # using numbers now
#alphabet = '0123456789'
repeats = 3
#targ_length = [10**10]
#targ_length = [10**10, 10**20]
#targ_length = [10**10, 10**20, 10**30, 10**40, 10**50]
mut_rate = [0, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1]
#mut_rate = [0.202, 0.404]
#mut_rate = [0, 0.00001, 0.00002, 0.00003, 0.00004, 0.00005, 0.00006, 0.00007, 0.00008, 0.00009, 0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

offs = 100

###

#set up a Pandas dataframe

###
raw_data = pd.DataFrame(columns = ['target','original_parent','parent','input_len','n_offspring','mutate_rate','gen','best_baseline'])

###

#Run the initial broad log range of mutation rates

###

for tar in target_list:
        #for off in offs:
            for mut in mut_rate:
                for rep in range(repeats):
                    data = []
                    data = data_weasel(str(tar), offs, mut)

                    raw_data = raw_data.append([data], ignore_index=True)

                    #print('Data Line from data_weasel')
                    print(data)


###

#While loop to optimize the muation rate

###

for n in range(10):
        #Convert the data to the correct formats
        raw_data['input_len'] = pd.to_numeric(raw_data['input_len'])
        raw_data['n_offspring'] = pd.to_numeric(raw_data['n_offspring'])
        raw_data['mutate_rate'] = raw_data['mutate_rate'].astype(float) #pd.to_numeric(raw_data['mutate_rate'])
        raw_data['gen'] = pd.to_numeric(raw_data['gen'])
        raw_data['best_baseline'] = pd.to_numeric(raw_data['best_baseline'])


        ###
        #This bit is now defunct
        # add column for % hit from target to best hit
        #raw_data['percent_hit'] = raw_data['best_baseline'] / raw_data['input_len']
        ###

        # look at data types and state of columns
        #print('raw_data DF head and dtypes')
        #print(raw_data['mutate_rate'])
        #print(raw_data.head())
        #print(raw_data.dtypes)

        ###

        # Want to reshape raw_data to look like: len, n_offspring, mutate_rate, mean_gen

        ###
        results = raw_data.groupby(['input_len', 'n_offspring', 'mutate_rate'])[['gen']].mean().reset_index()

        #print('results DF and dtypes')
        #print(results)
        #print(results.dtypes)

        ###

        # want to optimize mutation rate for each string length

        ###
        string_lengths = []
        str_lengths = results['input_len'].unique()
        for i in str_lengths:
            string_lengths.append(i)
        print('string lengths')
        print(string_lengths)
        print(len(string_lengths))

        targ_counter = 0
        for i in string_lengths:
            print('for i in string_lengths')
            print(i)

            #calculate mean for each string length and mutation rate
            rates = results.loc[results['input_len'] == i, 'mutate_rate'].tolist()
            mean_gens = (results.loc[results['input_len'] == i, 'gen']).tolist()
            #Work out where in the list of mutation rates the mean is
            mean_place = mean_gens.index(min(mean_gens))
            #Find one mutation rate either side
            mean_place_under = mean_place - 1
            mean_place_over = mean_place + 1
            under_rate = rates[mean_place_under]
            over_rate = rates[mean_place_over]
            #get a new range of mutation rates between those two points
            avg_rate = under_rate + over_rate
            new_rates = [(avg_rate * 0.2), (avg_rate * 0.4), (avg_rate * 0.6), (avg_rate * 0.8)]
            print('new mut_rates')
            print(under_rate)
            print(over_rate)
            print(avg_rate)
            print(avg_rate/2)
            print(new_rates)

            ###

            #tar now wants to be same index of targ lengths that corresponds to index of i in string_legths

            ###


            tar = target_list[targ_counter]
            #increase targ counter
            targ_counter += 1

            #for tar in targ_length:
                    # for off in offs:
            for mut in new_rates:
                        for rep in range(repeats):
                            data = []
                            data = data_weasel(str(tar), offs, mut)
                            raw_data = raw_data.append([data], ignore_index=True)

                            print(data)



###

# Plot the results


#add column for % hit from target to best hit
raw_data['percent_hit']= raw_data['best_baseline']/raw_data['input_len']



#Want to reshape raw_data to look like: len, n_offspring, mutate_rate, mean_gen

results = raw_data.groupby(['input_len', 'n_offspring', 'mutate_rate'])[['gen']].mean().reset_index()


###

# gen column of results = mean generations

###

y_lengths = []
str_lengths = results['input_len'].unique()
for i in str_lengths:
    y_lengths.append(i)
#print(y_lengths)
#print(len(y_lengths))
legends = []
for i in y_lengths:
    power = 0
    x = results.loc[results['input_len'] == i, 'mutate_rate']
    y = 1/(results.loc[results['input_len']==i, 'gen'])
    power = i
    legends.append(str(power) + ' letters')

    plt.plot(x,y, marker = 'o')




plt.xscale('log')
plt.yscale('log')

plt.title('Increaing mutation rate (0-1)')
plt.xlabel('Mutation Rate')
plt.ylabel('Generations')
plt.legend(legends, loc=0 )

plt.show()

