import itertools
from collections import Counter
from random import choice

class Node:
    def __init__(self, data="", pos=None, neg=None):
        self.data = data
        self.positive_child = pos
        self.negative_child = neg


class Record:

    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root):
        self.__root = root

    def is_leaf(self, negative_child, positive_child):
        """
        this function is a method that checks if the given node is a leaf,
        and if so returns True. if it is not it returns False
        :param node: a node to be checked
        :param child_list: a list of the node's children
        :return: True if node is leaf, False if isn't
        """
        if negative_child == None or positive_child == None:
            return True
        else:
            return False

    def _diagnose_helper(self, node, symptoms_list):
        """
        this is an aid function for the 'diagnose' function. it uses recursion
        in order to get to search every node's data in the symptoms list, so
        it goes over all nodes and returns the data of the right node.
        :param node: the root node, where the search is starting from.
        :param symptoms_list: a list of symptoms, received as an argument
        from the 'diagnose' function.
        :return: the right node's data (=the right illness)
        """
        if not symptoms_list:
            # if list is empty
            if node.negative_child:
                return self._diagnose_helper(node.negative_child, symptoms_list)
            return node.data
        if node.negative_child == None or node.positive_child == None:
            # base case: if the node is a leaf, it is the patient's illness
            return node.data
        if node.data in symptoms_list:
            # recursive call-  if the node's data is in [symptoms], the answer
            # is yes, so the node's positive child should be searched.
            return self._diagnose_helper(node.positive_child, symptoms_list)
        else:
            # negative recursive call- if the node's data isn't in [symptoms],
            # the answer is No and the negative child should be searched
            return self._diagnose_helper(node.negative_child, symptoms_list)

    def diagnose(self, symptoms):
        """
        this function gets a list of symptoms and diagnoses the patient's
        illness based on the symptoms he has and using a binary search tree.
        it uses an aid function called 'binary_search'
        :param symptoms: a list of symptoms
        :return: the patient's illness based on his symptoms
        """
        return self._diagnose_helper(self.__root, symptoms)

    def calculate_error_rate(self, records):
        """
        this function gets a list of records- list of lists. in every list
        appears a name of an illness and various symptoms of the illness.
        it counts the amount of wrong diagnoses and returns the error rate,
        which is the ratio between the amount of errors and the num of cases.
        :param records: a list of instances of class Record.
        :return: ratio between number of wrong diagnoses and the number of
        cases inputed in [records]
        """
        case_amount = len(records)  # every item in [records] is a case
        errors_count = 0
        for case in records:  # iterates over the list of cases- [records]
            illness = case.illness
            symptoms = case.symptoms
            if illness != self.diagnose(symptoms):
                # checks if the function diagnose returns the case's
                # illness for it's [symptoms]
                errors_count += 1
        return errors_count / case_amount  # divides and returns the ratio

    def node_check(self, node, illness_list):
        """
        this is an aid function for 'all_illnesses'. it uses recursion in
        order to get to all leaves of the tree.
        :param node:
        :param illness_list:
        :return:
        """
        if self.is_leaf(node.negative_child, node.positive_child):
            # if node is a leaf, the node's data is appended to illness_list
            return (illness_list + [node.data])
        return self.node_check(node.negative_child, illness_list) + \
               self.node_check(node.positive_child, illness_list)

    def all_illnesses(self):
        """
        this function gets to every leaf and returns a list of all of the
        leave's data (all illnesses). it uses the aid function node_check
        :return: a list of all illnesses
        """
        illness_list = []
        illness_list = sorted(list(set(self.node_check(self.__root, illness_list))))
        return illness_list

    def most_common_illness(self, records):
        """
        this function gets a list of record instances, iterates over every
        item in in the list (every medical case) and returns the one that
        is most common if you call the 'diagnose' func over the case
        :param records: a list of class Records instances
        :return: the most common illness
        """
        illness_dict = {}
        for case in records:
            illness = case.illness
            if illness in illness_dict:
                illness_dict[illness] += 1
            else:
                illness_dict[illness] = 1
        return max(illness_dict, key=illness_dict.get)

    def _paths_helper(self, cur_node, cur_path_list, illness):
        """
        this function is an aid function for the paths_to_illness function.
        it uses recursion in order to get to all leaves, and if the leaf's
        data is the wanted illness, it returns the list of the right path
        :param cur_node: the checked node
        :param cur_path_list: the being-built list of the current path
        :param illness: the searched illness
        :return: a list of lists of the different paths to the wanted illness
        """
        if self.is_leaf(cur_node.negative_child, cur_node.positive_child):
            # base case- if node is leaf
            if cur_node.data == illness:
                return [cur_path_list]
            else:
                return []
        else:  # two recursive calls- each for every of the node's children
            return self._paths_helper(cur_node.negative_child, cur_path_list
                                      + [False], illness) + \
                   self._paths_helper(cur_node.positive_child, cur_path_list
                                      + [True], illness)

    def paths_to_illness(self, illness):
        """
        this function returns a list of all paths to a given illness. this
        function uses the aid function '_paths_helper'
        :param illness: a given illness
        :return: a list of all paths to the illness
        """
        return self._paths_helper(self.__root, [], illness)


def node_generator(symptoms, symptom_ind, cur_path_list, records):
    """
    this function is an aid function for the build_tree function. it uses
    recursion in order to build the tree based on the given symptoms list,
    and in order to decide which illness to give to a leaf it calls a
    different function named "illness_finder". this function also builds a
    path-list for every leaf, which is provided for the illness_finder
    function in order to decide what illness to give to a leaf.
    :param symptoms: a list of symptoms from the call to the build_tree
    function
    :param symptom_ind: the index of the specific symptom the function was
    called with
    :param cur_path_list: received as an empty list, filled every time the
    function is called with the appropriate boolean value (True/False)
    :param records: the received list of class Record instances
    :return: root of the built tree
    """
    if symptom_ind == len(symptoms) - 1:
        #base case- the tree is built from bottom to top.
        cur_node = Node(str(symptoms[symptom_ind]),
                        Node(illness_finder(cur_path_list+[True], records, symptoms), None, None),
                        Node(illness_finder(cur_path_list+[False], records, symptoms), None, None))
        return cur_node #returns the deepest none-leaf node
        # whose children are supplied by an aid function
    else: # recursive call- building nodes from bottom to top using the
        # deepest none-leaf node, which is returned by the base case
        father = Node(str(symptoms[symptom_ind]),
                      node_generator(symptoms, symptom_ind + 1,
                                     cur_path_list+[True], records),
                      node_generator(symptoms, symptom_ind + 1,
                                     cur_path_list+[False], records))
        return father #returns the root of the tree


def illness_finder(path_list, records, symptoms):
    """
    this is an aid function for the node_generator function,
    which calculates the most suitable data for a leaf and returns it based
    on the route to the leaf and the list of symptoms and records.
    :param path_list: a list of True's and False's that represent the path
    to the leaf
    :param records: the records list provided from the main 'build_tree'
    function.
    :param symptoms: the symptoms list provided from the main 'build_tree'
    function
    :return: the appropriate name for a leaf
    """
    suspected_cases = records[:]
    for case in records: #iterating over cases in records
        for ind, decision in enumerate(path_list): #iterating over different
            #  depths in the path to the leaf
            if decision:
                if symptoms[ind] not in case.symptoms or not symptoms:
                    #condition- if the symptom was answered 'yes' and is not in
                    # the illness's symptoms
                    if case in suspected_cases:
                        suspected_cases.remove(case)
                        break
            elif symptoms:
                if symptoms[ind] in case.symptoms:
                    # condition- if the symptom was answered 'no' and is in
                    # the illness's symptoms
                    if case in suspected_cases:
                        suspected_cases.remove(case)
    if not suspected_cases:
        rand_record = choice(records)
        return rand_record.illness
    relevant_list = []
    for relevant_case in suspected_cases:
        #iterating over the relevant cases and building a list of the
        # relevant illnesses
        relevant_list.append(relevant_case.illness)
    filtered_list = Counter(relevant_list).most_common(1)
    return filtered_list[0][0] #returns the most suitable illness for the leaf


def build_tree(records, symptoms):
    """
    this function builds a tree using an aid function, nodes_generator,
    and returns the root of the tree
    :param records: a list of class Record instances
    :param symptoms: a list of different symptoms for a certain illness
    :return: the root of the built tree
    """
    root = node_generator(symptoms, 0, [], records)
    return root


def optimal_tree(records, symptoms, depth):
    """
    this function builds different trees based on a records list, symptoms
    list and a given depth and returns the root of the tree with the least
    wrong diagnoses.
    :param records: a list of class Record instances
    :param symptoms: a list of different symptoms for a certain illness
    :return: the root of the best tree (errors-rate wise)
    """
    #defining value for grading trees
    best_rate = 1
    best_root = None
    sub_symp = itertools.combinations(symptoms, depth)
    for sub_list in sub_symp: #itereating over the right sized lists
        node_type_root = build_tree(records, sub_list)
        cur_root = Diagnoser(node_type_root)
        error_rate = cur_root.calculate_error_rate(records)
        if error_rate < best_rate: #checks if this tree is the best so far
            best_rate = error_rate #if it is- set it as the best one so far
            best_root = node_type_root
    return best_root #returns the best tree's root


if __name__ == "__main__":
    # Manually build a simple tree.
    #                cough
    #          Yes /       \ No
    #        fever           healthy
    #   Yes /     \ No
    # influenza   cold

    flu_leaf = Node("influenza", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    healthy_leaf = Node("healthy", None, None)
    root = Node("cough", inner_vertex, healthy_leaf)
    diagnoser = Diagnoser(root)

    flu_leaf = Node("influenza", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    healthy_leaf = Node("healthy", None, None)
    root = Node("cough", inner_vertex, healthy_leaf)


     # # Simple test
    diagnosis = diagnoser.diagnose(["cough"])
    if diagnosis == "cold":
        print("Test passed")
    else:
       print("Test failed. Should have printed cold printed: ", diagnosis)
     # Add more tests for sections 2-7 here.
