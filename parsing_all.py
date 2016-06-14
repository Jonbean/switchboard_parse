'''
PART ONE:
Terminals Parsing
'''
import os
import xml.etree.ElementTree as ET
import sys


#get_IDdict will return built up IDdict and IDlist
def get_IDdict(root, IDdict, IDlist):
    for child in root:
        if child.tag == 'word':
            wordid = child.get(namespaceIdentifier+'id')
            IDdict[wordid] = []
            IDlist.append(wordid)
            #attach the word
            IDdict[wordid].append(child.get('orth'))
            #attach pos tag
            IDdict[wordid].append(child.get('pos'))
            #attach start end time
            IDdict[wordid].append(child.get(namespaceIdentifier+'start'))
            IDdict[wordid].append(child.get(namespaceIdentifier+'end'))

            #build Phonedict if link exists
            phoneword = child.find(namespaceIdentifier+'pointer')
            if phoneword != None:
                phoneword_ID = phoneword.get('href').split('#')[1][3:-1]
                Phoneword_dict[phoneword_ID] = wordid
            else:
                continue

        if child.tag == 'punc':
            wordid = child.get(namespaceIdentifier+'id')
            IDdict[wordid] = []
            #attach the word
            IDlist.append(wordid)
            IDdict[wordid].append(child.text)
            #attach pos tag
            IDdict[wordid].append(None)
            #attach start end time
            IDdict[wordid].append(None)
            IDdict[wordid].append(None)
        if child.tag == 'sil':
            wordid = child.get(namespaceIdentifier+'id')
            IDdict[wordid] = []
            IDlist.append(wordid)
            IDdict[wordid].append('SILENCE')
            #attach pos tag
            IDdict[wordid].append(None)
            #attach start end time
            IDdict[wordid].append(None)
            IDdict[wordid].append(None)
        if child.tag == 'trace':
            wordid = child.get(namespaceIdentifier+'id')
            IDdict[wordid] = []
            IDlist.append(wordid)
            IDdict[wordid].append('TRACE')
            #attach pos tag
            IDdict[wordid].append(None)
            #attach start end time
            IDdict[wordid].append(None)
            IDdict[wordid].append(None)
        else:
            continue
    return IDdict, IDlist

# print out sentence with word-level attributes
# print out with space between sentences
def pretty_print(AIDdict, AIDlist, BIDdict, BIDlist):
    indexA = 0
    indexB = 0
    inwhich = ''
    if AIDlist[0][1:].split('_')[0] == '1':
        inwhich = 'A'
    else:
        inwhich = 'B'

    while indexA < len(AIDlist) - 1 or indexB < len(BIDlist) - 1:
        if inwhich == 'A':
            if indexA >= len(AIDlist) - 1 and indexB < len(BIDlist):
                print 'A', AIDlist[indexA],
                for element in AIDdict[AIDlist[indexA]]:
                    if type(element) is tuple:
                        for subele in element:
                            print subele,
                    elif type(element) is list:
                        for subele in element:
                            print subele,
                    else:
                        print element,
                print ""
                inwhich = 'B'
                print ''
                continue

            print 'A', AIDlist[indexA],
            for element in AIDdict[AIDlist[indexA]]:
                if type(element) is tuple:
                    for subele in element:
                        print subele,
                elif type(element) is list:
                    for subele in element:
                        print subele,
                else:
                    print element,
            print ""
            nextsentnum = int(AIDlist[indexA + 1].split('_')[0][1:])
            sentnum = int(AIDlist[indexA].split('_')[0][1:])
            if nextsentnum - sentnum > 1:
                inwhich = 'B'
                print ''
            if nextsentnum - sentnum == 1:
                print ''
            indexA += 1
            # if indexA >= len(AIDlist) and indexB >= len(BIDlist):
            #     break

        if inwhich == 'B':
            if indexB >= len(BIDlist) - 1 and indexA < len(AIDlist):
                print 'B', BIDlist[indexB],
                for element in BIDdict[BIDlist[indexB]]:
                    if type(element) is tuple:
                        for subele in element:
                            print subele,
                    elif type(element) is list:
                        for subele in element:
                            print subele,
                    else:
                        print element,
                print ""
                inwhich = 'A'
                print ''
                continue

            print 'B', BIDlist[indexB],
            for element in BIDdict[BIDlist[indexB]]:
                if type(element) is tuple:
                    for subele in element:
                        print subele,
                elif type(element) is list:
                    for subele in element:
                        print subele,
                else:
                    print element,
            print ""
            nextsentnum = int(BIDlist[indexB + 1].split('_')[0][1:])
            sentnum = int(BIDlist[indexB].split('_')[0][1:])
            if nextsentnum - sentnum > 1:
                inwhich = 'A'
                print ''
            if nextsentnum - sentnum == 1:
                print ''
            indexB += 1
            # if indexA >= len(AIDlist) and indexB >= len(BIDlist):
            #     break


def attach_to_terminal_func(termi_attribute_dict, IDdict):
    for ID in IDdict:
        IDdict[ID].append(termi_attribute_dict[ID])

def None_dialfile_dict_builder(IDdict):
    termi_dialAct_dict = {}
    #second attach termi_wordID who has not been attached in diaActdict
    for key in IDdict:
        if key not in termi_dialAct_dict:
            termi_dialAct_dict[key] = (None, None, None)
    return termi_dialAct_dict

def get_dialActDict(root):
    #diaActdict structure:
    #{(daID, niteType, swbdType): [word_id, word_id, ..., word_id]}
    diaActdict = {}
    for child in root:
        #find dialAct first
        niteType = child.get('niteType')
        swbdType = child.get('swbdType')
        daId = child.get(namespaceIdentifier+'id')
        diaActdict[(daId, niteType, swbdType)] = []
        pointers_to_word = child.findall(namespaceIdentifier+'child')
        for pointer in pointers_to_word:
            word_id = pointer.get('href').split('#')[1][3:-1]
            diaActdict[(daId, niteType, swbdType)].append(word_id)
    return diaActdict

#attach diaAct to word list
def attach_diaAct_to_terminal(termi_dial_dict, IDdict):
    for key in IDdict:
        IDdict[key].append(termi_dial_dict[key])



def terminal_diaAct_dict_builder(diaActdict, IDdict):
    #termi_dialAct_dict structure:
    #{terminal_wordID: (daID, niteType, swbdType)}
    termi_dialAct_dict = {}

    #first attach diaActdict termi_wordID
    for key in diaActdict:
        for word_id in diaActdict[key]:
            termi_dialAct_dict[word_id] = key

    #second attach termi_wordID who has not been attached in diaActdict
    for key in IDdict:
        if key not in termi_dialAct_dict:
            termi_dialAct_dict[key] = (None, None, None)

    return termi_dialAct_dict
def None_dflfile_dict_builder(IDdict):
    termi_dfl_dict = {}
    for key in IDdict:
        if key not in reparandum_dict and key not in repair_dict:
            termi_dfl_dict[key] = None

    return termi_dfl_dict


def get_dfl_dict(root):
    reparandum_dict = {}
    repair_dict = {}
    for child in root:
        #since disfluency is in tree structrue, the depth are not decided
        #we use iter() to convert every disfluency child into a list.
        all_children = list(child.iter())
        reparandum_depth = 1


        for subchild in all_children:
            if subchild.tag == 'reparandum':
                if subchild.find(namespaceIdentifier+'child') == None:
                    reparandum_depth +=1
                else:
                    words = []
                    termis = subchild.findall(namespaceIdentifier+'child')
                    last_word_ID = termis[-1].get('href').split('#')[1][3:-1]
                    for word in termis:
                        words.append(word.get('href').split('#')[1][3:-1])

                    reparandum_dict[words[0]] = reparandum_depth
                    if len(words) > 1:
                        for i in range(1,len(words)):
                            reparandum_dict[words[i]] = '+'

            elif subchild.tag == 'repair':
                if subchild.find(namespaceIdentifier+'child') == None:
                    continue
                else:
                    repair_words = []
                    termis = subchild.findall(namespaceIdentifier+'child')
                    for word in termis:
                        repair_words.append(word.get('href').split('#')[1][3:-1])

                    repair_dict[repair_words[-1]] = reparandum_depth
                    if len(repair_words) > 1:
                        for i in range(len(repair_words) - 1):
                            repair_dict[repair_words[i]] = '-'
                    reparandum_depth -= 1
    return reparandum_dict, repair_dict


#create terminals disfluency dict
def terminal_dfl_dict_builder(reparandum_dict, repair_dict, IDdict):
    #termi_dfl_dict structure:
    #{termi_wordID: disfluency_label}
    termi_dfl_dict = {}
    for key in reparandum_dict:
        termi_dfl_dict[key] = reparandum_dict[key]
    for key in repair_dict:
        termi_dfl_dict[key] = repair_dict[key]

    for key in IDdict:
        if key not in reparandum_dict and key not in repair_dict:
            termi_dfl_dict[key] = None

    return termi_dfl_dict

'''======================part_one======================'''
#namespace is retrieved by hand ahead, it's correct
namespaceIdentifier = '{http://nite.sourceforge.net/}'

#for iteration purpose, we split filename according to
#their name pattern, only the first part varies
swnumb = sys.argv[1]

#use ET package retrieve tree structure data for A and B speaker
Afilepath = os.path.join(os.getcwd(), 'terminals', swnumb + '.A.terminals.xml')
Bfilepath = os.path.join(os.getcwd(), 'terminals', swnumb + '.B.terminals.xml')
Atree = ET.parse(Afilepath)
Btree = ET.parse(Bfilepath)

Aroot = Atree.getroot()
Broot = Btree.getroot()

#IDdict is a dictionary for quick checking attribute of each word
#IDdict structure:
#{terminal_wordID: ['word', 'pos', 'starttime', 'endtime', ]}
AIDdict = {}
BIDdict = {}

#IDlist is an array, for sequence record, because IDdict will loss sequence info
AIDlist = []
BIDlist = []

#phoneword_dict is a dict to link between terminal and phonewords transcripts
#we don't distinguish A and B for A and B has different wordID, they won't conflict
Phoneword_dict = {}

AIDdict, AIDlist = get_IDdict(Aroot, AIDdict, AIDlist)
BIDdict, BIDlist = get_IDdict(Broot, BIDdict, BIDlist)
'''======================part_two======================'''

try:
    #adding dialogue act tags into original dataset

    Afilepath = os.path.join(os.getcwd(), 'dialAct',swnumb + '.A.dialAct.xml')
    Bfilepath = os.path.join(os.getcwd(), 'dialAct',swnumb + '.B.dialAct.xml')

    Atree = ET.parse(Afilepath)
    Aroot = Atree.getroot()
    Btree = ET.parse(Bfilepath)
    Broot = Btree.getroot()
    #get dialAct dictionary for speaker A and B
    A_dial_Act_dict = get_dialActDict(Aroot)
    B_dial_Act_dict = get_dialActDict(Broot)

    #get termi_diaAct_dict
    Atermi_dialAct_dict = terminal_diaAct_dict_builder(A_dial_Act_dict, AIDdict)
    Btermi_dialAct_dict = terminal_diaAct_dict_builder(B_dial_Act_dict, BIDdict)

    # #attach to terimal_wordID for pretty print
    # attach_diaAct_to_terminal(Atermi_dialAct_dict, AIDdict)
    # attach_diaAct_to_terminal(Btermi_dialAct_dict, BIDdict)


    # pretty_print(AIDdict, AIDlist, BIDdict, BIDlist)
except:
    Atermi_dialAct_dict = None_dialfile_dict_builder(AIDdict)
    Btermi_dialAct_dict = None_dialfile_dict_builder(BIDdict)

'''======================part_three======================'''
try:
    Afilepath = os.path.join(os.getcwd(), 'disfluency', swnumb+'.A.disfluency.xml')
    Bfilepath = os.path.join(os.getcwd(), 'disfluency', swnumb+'.B.disfluency.xml')
    Atree = ET.parse(Afilepath)
    Aroot = Atree.getroot()
    Btree = ET.parse(Bfilepath)
    Broot = Btree.getroot()


    #create 2 list to record the position of reparandum and repair in
    #terminal

    #get reparandum_dict and repair_dict
    Areparandum_dict, Arepair_dict = get_dfl_dict(Aroot)
    Breparandum_dict, Brepair_dict = get_dfl_dict(Broot)

    #link termi_wordID to reparandum and repair
    Atermi_dfl_dict = terminal_dfl_dict_builder(Areparandum_dict, Arepair_dict, AIDdict)
    Btermi_dfl_dict = terminal_dfl_dict_builder(Breparandum_dict, Brepair_dict, BIDdict)

    # #attach reparandum/repair for pretty print
    # attach_to_terminal_func(Atermi_dfl_dict, AIDdict)
    # attach_to_terminal_func(Btermi_dfl_dict, BIDdict)

    # pretty_print(AIDdict, AIDlist, BIDdict, BIDlist)
except:
    Atermi_dfl_dict = None_dflfile_dict_builder(AIDdict)
    Btermi_dfl_dict = None_dflfile_dict_builder(BIDdict)
'''======================part_four======================'''
'''
PART FOUR:
Syntax Parsing
'''
#syntax_dict structure
#{termi_wordID: syntax_label}
syntax_dict = {}

def traverse_func(root, ancestors):
    if root.tag == namespaceIdentifier+'child':
        #if reached leaves, return its' word id in terminals
        ID = root.get('href').split('#')[1][3:-1]
        syntax_dict[ID] = ancestors
    else:
        if root.get('cat') != None:
            ancestors = ancestors + str(root.get('cat')) + '('+str(root.get(namespaceIdentifier+'id'))+')' + '|'
        for child in root:
                traverse_func(child, ancestors)

#termi_syn_dict structure:
#{sytax_ID: [termi_wordID, termi_wordID, .. , termi_wordID]}
termi_syn_dict = {}

def traverse_get_synId_func(root, ancestors):
    if root.tag == namespaceIdentifier+'child':
        #if reached leaves, return its' word id in terminals
        termi_wordID = root.get('href').split('#')[1][3:-1]
        for syn_ID in ancestors:
            termi_syn_dict[syn_ID].append(termi_wordID)
    else:
        node_ID = root.get(namespaceIdentifier+'id')
        if node_ID != None:
            ancestors.append(node_ID)
            termi_syn_dict[node_ID] = []
        for child in root:
            traverse_get_synId_func(child, ancestors)


def get_syntax_termi_dict(root):
    for child in root:
        #all child taged 'parse', one child denotes one sentence, namely a syntax tree
        #structure:
        '''
              <'parse'>(sentence)
              /                \
             /                  \
           <nt>                <nt>
          /    \              /    \
         word  word          <nt>  word
                           /  |  \
                        word word <nt>
                                  ...
        (<nt> denotes a syntax label)
        '''
        for subchild in child:
            traverse_get_synId_func(subchild, [])


def get_syntax_dict(root):
    for child in root:
        #all child taged 'parse', one child denotes one sentence, namely a syntax tree
        #structure:
        '''
              <'parse'>(sentence)
              /                \
             /                  \
           <nt>                <nt>
          /    \              /    \
         word  word          <nt>  word
                           /  |  \
                        word word <nt>
                                  ...
        (<nt> denotes a syntax label)
        '''
        for subchild in child:
            traverse_func(subchild, '')


# attach syntax label to terminals
def termi_syntax_dict_builder(syntaxDict, IDdict):
    termi_syn_dict = {}
    for key in IDdict:
        if key not in syntaxDict:
            termi_syn_dict[key] = 'No_Syntax_Info'
        else:
            termi_syn_dict[key] = syntaxDict[key]
    return termi_syn_dict

try:
    Afilepath = os.path.join(os.getcwd(), 'syntax', swnumb+'.A.syntax.xml')
    Bfilepath = os.path.join(os.getcwd(), 'syntax', swnumb+'.B.syntax.xml')
    Atree = ET.parse(Afilepath)
    Aroot = Atree.getroot()
    Btree = ET.parse(Bfilepath)
    Broot = Btree.getroot()

    get_syntax_dict(Aroot)
    get_syntax_dict(Broot)

    #to get termi_syn_dict
    get_syntax_termi_dict(Aroot)
    get_syntax_termi_dict(Broot)


    Atermi_syn_dict = termi_syntax_dict_builder(syntax_dict, AIDdict)
    Btermi_syn_dict = termi_syntax_dict_builder(syntax_dict, BIDdict)

    # attach_to_terminal_func(Atermi_syn_dict, AIDdict)
    # attach_to_terminal_func(Btermi_syn_dict, BIDdict)

    # pretty_print(AIDdict, AIDlist, BIDdict, BIDlist)
except:
    pass

'''======================part_five======================'''
'''
PART FIVE:
Movement Parsing
'''

#synword_dict structure
#{syn_ID: [terminal_wordID, terminal_wordID]}
synword_dict = {}

#move_dict structure
#{terminal_wordID: (wordID, label)}
move_dict = {}


def traverse_get_syn_word_dict(root, parent):
    if root.tag == namespaceIdentifier+'child':
        synword_dict[parent.get(namespaceIdentifier+'id')].append(root.get('href').split('#')[1][3:-1])

    else:
        syn_ID = root.get(namespaceIdentifier+'id')
        synword_dict[syn_ID] = []
        for child in root:
            traverse_get_syn_word_dict(child, root)

#First: build syntax-word dict({syntaxID: [terminal_wordID, termninal_wordID, ...]})
def get_syn_word_dict(root):
    for child in root:
        for subchild in child:
            traverse_get_syn_word_dict(subchild, child)

#Second: build syntax-movement dict({source(syntax(words)): target(word) })
def get_syntax_move_dict(root):
    for child in root:
        synID = ''
        wordID = ''
        label = child.get('label')
        for subchild in child:
            if subchild.get('role') == 'source':
                synID = subchild.get('href').split('#')[1][3:-1]
            else:
                wordID = subchild.get('href').split('#')[1][3:-1]
            for word in synword_dict[synID]:
                move_dict[word] = (wordID, label)


#Third: attach terminals with the movement words
def termi_move_dict_builder(move_dict, IDdict):
    for key in IDdict:
        if key not in move_dict:
            move_dict[key] = (None, None)

try:
    Afilepath = os.path.join(os.getcwd(), 'syntax', swnumb+'.A.syntax.xml')
    Bfilepath = os.path.join(os.getcwd(), 'syntax', swnumb+'.B.syntax.xml')
    Atree = ET.parse(Afilepath)
    Aroot = Atree.getroot()
    Btree = ET.parse(Bfilepath)
    Broot = Btree.getroot()

    Amove_file = os.path.join(os.getcwd(), 'movement', swnumb+'.A.movement.xml')
    Bmove_file = os.path.join(os.getcwd(), 'movement', swnumb+'.B.movement.xml')
    Amove_tree = ET.parse(Amove_file)
    Amove_root = Amove_tree.getroot()
    Bmove_tree = ET.parse(Bmove_file)
    Bmove_root = Bmove_tree.getroot()


    get_syn_word_dict(Aroot)
    get_syn_word_dict(Broot)

    get_syntax_move_dict(Amove_root)
    get_syntax_move_dict(Bmove_root)

    termi_move_dict_builder(move_dict, AIDdict)
    termi_move_dict_builder(move_dict, BIDdict)

    # attach_to_terminal_func(move_dict, AIDdict)
    # attach_to_terminal_func(move_dict, BIDdict)

    # pretty_print(AIDdict, AIDlist, BIDdict, BIDlist)
except:
    termi_move_dict_builder(move_dict, AIDdict)
    termi_move_dict_builder(move_dict, BIDdict)

'''======================part_six======================'''
'''
PART SIX:
Kontrast Parsing
'''
def None_kontrastfile_dict_builder(AIDdict, BIDdict):
    terminal_kontrast_trigger_dict = {}
    for ID in AIDdict:
        if ID not in terminal_kontrast_trigger_dict:
            terminal_kontrast_trigger_dict[ID] = [None, None]

    for ID in BIDdict:
        if ID not in terminal_kontrast_trigger_dict:
            terminal_kontrast_trigger_dict[ID] = [None, None]

    return terminal_kontrast_trigger_dict


def termi_kontrast_dict_builder(kontrast_root, trigger_root, AIDdict, BIDdict):
    #kontrast_termi_dict structure:
    #{kontrast_ID: (termi_wordID, kontrast_type)}
    kontrast_terim_dict = {}

    #terminal_kontrast_trigger_dict structure
    #{termi_wordID: [kontrast_type, trigger/referent, word_point_to]}
    terminal_kontrast_trigger_dict ={}
    for child in kontrast_root:
        kontrasttype = child.get('type')
        kontrast_ID = child.get(namespaceIdentifier+'id')
        for subchild in child:
            kontrast_terim_dict[kontrast_ID] = (subchild.get('href').split('#')[1][3:-1], kontrasttype)

    for child in trigger_root:
        trigger_ID = ''
        referent_ID = ''
        link_word_ids = []
        for subchild in child:
            kontrast_ID = subchild.get('href').split('#')[1][3:-1]
            termi_wordID = kontrast_terim_dict[kontrast_ID][0]
            kontrast_type = kontrast_terim_dict[kontrast_ID][1]
            link_word_ids.append(termi_wordID)
            if subchild.get('role') == 'trigger':
                terminal_kontrast_trigger_dict[termi_wordID] = [kontrast_type, 'trigger']
            else:
                terminal_kontrast_trigger_dict[termi_wordID] = [kontrast_type, 'referent']
        terminal_kontrast_trigger_dict[link_word_ids[0]].append(link_word_ids[1])
        terminal_kontrast_trigger_dict[link_word_ids[1]].append(link_word_ids[0])


    for ID in AIDdict:
        if ID not in terminal_kontrast_trigger_dict:
            terminal_kontrast_trigger_dict[ID] = [None, None]

    for ID in BIDdict:
        if ID not in terminal_kontrast_trigger_dict:
            terminal_kontrast_trigger_dict[ID] = [None, None]

    return terminal_kontrast_trigger_dict

try:
    kontrast_filepath = os.path.join(os.getcwd(), 'kontrast', swnumb+'.kontrast.xml')
    trigger_filepath = os.path.join(os.getcwd(), 'kontrast', swnumb+'.trigger.xml')
    kontrast_tree = ET.parse(kontrast_filepath)
    kontrast_root = kontrast_tree.getroot()
    trigger_tree = ET.parse(trigger_filepath)
    trigger_root = trigger_tree.getroot()


    terminal_kontrast_trigger_dict = termi_kontrast_dict_builder(kontrast_root, trigger_root, AIDdict, BIDdict)

    # attach_to_terminal_func(terminal_kontrast_trigger_dict, AIDdict)
    # attach_to_terminal_func(terminal_kontrast_trigger_dict, BIDdict)

    # pretty_print(AIDdict, AIDlist, BIDdict, BIDlist)
except:

    terminal_kontrast_trigger_dict = None_kontrastfile_dict_builder(AIDdict, BIDdict)

'''======================part_seven======================'''
'''
PART EIGHT:
Phoneword and Syllables
'''

def None_phonefile_dict_builder(IDdict):
    termi_phone_dict = {}
    for ID in IDdict:
        if ID not in termi_phone_dict:
            termi_phone_dict[ID] = 'No_syllable_Info'

    return termi_phone_dict

def None_syllablefile_dict_builder(IDdict):
    termi_syllable_dict = {}
    for ID in IDdict:
        if ID not in termi_syllable_dict:
            termi_syllable_dict[ID] = [None, [None, None]]

    return termi_syllable_dict

def termi_phone_dict_builder(phone_root, termi_syllable_dict, syllable_phone_dict, IDdict):
    termi_phone_dict = {}

    phones_dict = {}
    #phones_dict structure:
    #{Phone_ID: (phone_start, Phone_end)}
    for child in phone_root:
        phone_ID = child.get(namespaceIdentifier+'id')
        phone_start = child.get(namespaceIdentifier+'start')
        phone_end = child.get(namespaceIdentifier+'end')
        phones_dict[phone_ID] = (phone_start, phone_end)

    for termi_ID in termi_syllable_dict:
        #phone_string is a string variable to record phone start, end.
        phone_string = ''
        if termi_syllable_dict[termi_ID][0] == None:
            continue
        for syn_ID in termi_syllable_dict[termi_ID][1]:
            start_phoneID = syllable_phone_dict[syn_ID][0]
            end_phoneID = syllable_phone_dict[syn_ID][1]
            start_time = phones_dict[start_phoneID][0]
            end_time = phones_dict[end_phoneID][1]
            phone_string +='('+str(start_time)+'|'+str(end_time)+')'
        termi_phone_dict[termi_ID] = phone_string

    for ID in IDdict:
        if ID not in termi_phone_dict:
            termi_phone_dict[ID] = 'No_syllable_Info'

    return termi_phone_dict

def syllable_phone_dict_builder(syllable_root):
    # syllable_phone_dict structure
    # {syn_ID: (startphoneID, endphoneID)}
    syllable_phone_dict = {}
    for child in syllable_root:
        syn_ID = child.get(namespaceIdentifier+'id')
        for subchild in child:
            phoneIDs = subchild.get('href').split('#')[1]
            if '..' in phoneIDs:
                startphoneID = phoneIDs.split('..')[0][3:-1]
                endphoneID = phoneIDs.split('..')[1][3:-1]
                syllable_phone_dict[syn_ID] = (startphoneID, endphoneID)
            else:
                startphoneID = phoneIDs[3:-1]
                endphoneID = phoneIDs[3:-1]
                syllable_phone_dict[syn_ID] = (startphoneID, endphoneID)

    return syllable_phone_dict


def termi_syllable_dict_builder(phonewordroot, IDdict):
    # termin_syllable_dict structure:
    # {termi_wordID:[stressprofile, [syllable_ID, ... ,syllable_ID]]}
    termi_syllable_dict = {}

    for child in phonewordroot:
        phonID = child.get(namespaceIdentifier+'id')
        StressProfile = child.get('stressProfile')
        if StressProfile == '':
            StressProfile = None

        syllable_ID = []
        for subchild in child:
            syn_IDs = subchild.get('href').split('#')[1]
            if '..' in syn_IDs:
                #e.g. id(ms9A_sy1)..id(ms9A_sy2)
                #syn_ID = [id(ms9A_sy1), id(ms9A_sy2)]
                syn_ID = syn_IDs.split('..')
                start_ID = syn_ID[0][3:-1]
                end_ID = syn_ID[1][3:-1]

                ID = start_ID
                while ID != end_ID:
                    syllable_ID.append(ID)
                    ID = ID.split('sy')[0]+'sy' + str(int(ID.split('sy')[1])+1)
                syllable_ID.append(ID)
            else:
                syllable_ID.append(syn_IDs[3:-1])
        if syllable_ID == []:
            syllable_ID = None

        if phonID in Phoneword_dict:
            termi_syllable_dict[Phoneword_dict[phonID]] = []
            termi_syllable_dict[Phoneword_dict[phonID]].append(StressProfile)
            termi_syllable_dict[Phoneword_dict[phonID]].append(syllable_ID)

    for ID in IDdict:
        if ID not in termi_syllable_dict:
            termi_syllable_dict[ID] = [None, [None, None]]

    return termi_syllable_dict


def termi_syllable_dict_modify(termi_syllable_dict):
    #new_termi_syllable_dict structure:
    #{termi_ID : syllable}
    new_termi_syllable_dict = {}

    for ID in termi_syllable_dict:
        new_termi_syllable_dict[ID] = termi_syllable_dict[ID][0]

    return new_termi_syllable_dict
try:
    # we have Phoneword_dict, which links phoneword with terminal words
    # Phoneword_dict structure:
    # {PhonID: termi_wordID}
    #build phoneword, syllable hashmap!

    Afilepath = os.path.join(os.getcwd(), 'phonwords', swnumb+'.A.phonwords.xml')
    Bfilepath = os.path.join(os.getcwd(), 'phonwords', swnumb+'.B.phonwords.xml')
    Atree = ET.parse(Afilepath)
    Aroot = Atree.getroot()
    Btree = ET.parse(Bfilepath)
    Broot = Btree.getroot()

    Asynfilepath = os.path.join(os.getcwd(), 'syllables', swnumb+'.A.syllables.xml')
    Bsynfilepath = os.path.join(os.getcwd(), 'syllables', swnumb+'.B.syllables.xml')
    Asyntree = ET.parse(Asynfilepath)
    Asynroot = Asyntree.getroot()
    Bsyntree = ET.parse(Bsynfilepath)
    Bsynroot = Bsyntree.getroot()

    Aphonefilepath = os.path.join(os.getcwd(), 'phones', swnumb+'.A.phones.xml')
    Bphonefilepath = os.path.join(os.getcwd(), 'phones', swnumb+'.B.phones.xml')
    Aphonetree = ET.parse(Aphonefilepath)
    Aphoneroot = Aphonetree.getroot()
    Bphonetree = ET.parse(Bphonefilepath)
    Bphoneroot = Bphonetree.getroot()

    Atermi_syllable_dict = termi_syllable_dict_builder(Aroot, AIDdict)
    Asyn_phone_dict = syllable_phone_dict_builder(Asynroot)
    Atermi_phone_dict = termi_phone_dict_builder(Aphoneroot, Atermi_syllable_dict, Asyn_phone_dict, AIDdict)

    Btermi_syllable_dict = termi_syllable_dict_builder(Broot, BIDdict)
    Bsyn_phone_dict = syllable_phone_dict_builder(Bsynroot)
    Btermi_phone_dict = termi_phone_dict_builder(Bphoneroot, Btermi_syllable_dict, Bsyn_phone_dict, BIDdict)

    Atermi_syllable_dict = termi_syllable_dict_builder(Aroot, AIDdict)
    Btermi_syllable_dict = termi_syllable_dict_builder(Broot, BIDdict)

    Anew_termi_syllable_dict = termi_syllable_dict_modify(Atermi_syllable_dict)
    Bnew_termi_syllable_dict = termi_syllable_dict_modify(Btermi_syllable_dict)


    # attach_to_terminal_func(Atermi_syllable_dict, AIDdict)
    # attach_to_terminal_func(Btermi_syllable_dict, BIDdict)
    # attach_to_terminal_func(Atermi_phone_dict, AIDdict)
    # attach_to_terminal_func(Btermi_phone_dict, BIDdict)

    # pretty_print(AIDdict, AIDlist, BIDdict, BIDlist)
except:
    Atermi_phone_dict = None_phonefile_dict_builder(AIDdict)
    Btermi_phone_dict = None_phonefile_dict_builder(BIDdict)
    Atermi_syllable_dict = None_syllablefile_dict_builder(AIDdict)
    Btermi_syllable_dict = None_syllablefile_dict_builder(BIDdict)
    Anew_termi_syllable_dict = termi_syllable_dict_modify(Atermi_syllable_dict)
    Bnew_termi_syllable_dict = termi_syllable_dict_modify(Btermi_syllable_dict)




'''======================combination======================'''

attach_to_terminal_func(Atermi_dialAct_dict, AIDdict)
attach_to_terminal_func(Btermi_dialAct_dict, BIDdict)

attach_to_terminal_func(Atermi_dfl_dict, AIDdict)
attach_to_terminal_func(Btermi_dfl_dict, BIDdict)

attach_to_terminal_func(Atermi_syn_dict, AIDdict)
attach_to_terminal_func(Btermi_syn_dict, BIDdict)

attach_to_terminal_func(Anew_termi_syllable_dict, AIDdict)
attach_to_terminal_func(Bnew_termi_syllable_dict, BIDdict)

attach_to_terminal_func(Atermi_phone_dict, AIDdict)
attach_to_terminal_func(Btermi_phone_dict, BIDdict)

attach_to_terminal_func(move_dict, AIDdict)
attach_to_terminal_func(move_dict, BIDdict)

attach_to_terminal_func(terminal_kontrast_trigger_dict, AIDdict)
attach_to_terminal_func(terminal_kontrast_trigger_dict, BIDdict)

pretty_print(AIDdict, AIDlist, BIDdict, BIDlist)

