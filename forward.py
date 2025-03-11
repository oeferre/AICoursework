
import numpy
import heapq

facts = {}

# list of rules
# each rule is a tuple (body, head)
# body is a list of atoms (i.e., tuples with atom name as first element)
# head is a single tuple where the first element is the name of the atom, and the other elements are its arguments
# e.g., ([("Lecturer", "X")("Teaches", "X", "Y")], ("Module", "Y"))
# represents the rule Lecturer(x) & Teaches(x,y) -> Module(y)
rules = []

# facts is a dictionary where keys are atoms names and values are set of tuples representing their instances
# e.g., {"Lecturer" : {("fabio",),("marco",)}} represents Lecturer(fabio) and Lecturer(marco)

# simple function for adding facts
# the input is the name of the atom followed by its arguments
# e.g., ("Lecturer", "fabio") represents the atom Lecturer(fabio), ("Likes", "fabio", "chocolate") represents Likes(fabio,chocolate)
def add_fact(name, *args):
    global facts
    current_set = set()
    if name in facts.keys():
        current_set = facts[name]
    current_set.add(tuple(args))
    facts[name] = current_set

    
# simple function to add a rule
# see description above for the format of body and head
def add_rule(body, head):
    global rules
    rules += [(body, head)]


# recursive function to find all ways to instantiate a rule body based on currently known facts
# input:
#  - body of a rule (i.e., a list of atoms with variables)
#  - substitution we are currently trying to build (i.e., a dictionary where keys are variables and values represent what the variables are replaced with)
#  - all found substitutions (i.e., a list of complete substitutions)
def find_substitutions(body_to_check, current_sub, subs):
    global facts

    # base case 1
    # all atoms in the body have been successfully matched by the current substitution
    # add the substitution to the overall list of substitutions and return the list
    if body_to_check == []:
        subs += [current_sub]
        return subs

    # split the body into the atom to check and the rest, we will recurse on the rest to reach the base case 1
    atom, *rest = body_to_check
    # take the atom name and its arguments
    name, *args = atom

    # base case 2
    # if there is no instance for the atom, the substution fails
    # otherwise, collect all possible instances of the atom
    if name in facts.keys():
        matches = facts[name]
    else:
        return subs

    # loop to filter atom instances based on the current values assigned to variables
    for i in range(len(args)):
        var = args[i]
    
        if var in current_sub.keys():
            matches = set(filter(lambda x : True if x[i] == current_sub[var] else False, matches))

    # base case 3
    # if an atom has no instances left, then the current substituion fails
    if matches == []:
        return subs

    # loop over valid atom instances
    for match in matches:
        new_sub = current_sub.copy()

        for i in range(len(args)):
            var = args[i]
            # extend the current substitution with new varible bindings based on the atom instance
            if not (var in new_sub.keys()):
                new_sub[var] = match[i]

        # recursive call -- note that the call is within a for loop, which results in a backtracking approach
        subs = find_substitutions(rest, new_sub, subs)
        
    # return found substitutions
    return subs



# function that apply all found substitutions to the head of the rule to derive new facts
# input: a list of substitutions (each substitution is a dictionary) and the head of a rule
# output: true if a new fact was derived, false otherwise
def derive(substitutions, head):
    global facts

    # unapcking the head to get the atom name and its arguments
    name, *args = head

    result = set()

    # loop to create atom instances based on the different substitutions
    for sub in substitutions:
        # initialisation of an instance as an empty tuple
        instance = ()
        for i in args:
            # updating the instance with actual values based on the substitution under consideration
            instance += (sub[i],)
         
        result.add(instance)

    # check which instances are actually new
    if name in facts.keys():
         new_facts = result.difference(facts[name])
    else:
        facts[name] = result
        new_facts = result

    # return false if all facts are already known
    if new_facts == set():
        return False

    for i in new_facts:
        print(f'new fact {name}{i}')

    # update facts with new derived instances and return true
    facts[name] = facts[name].union(new_facts)
    return True



################
## Your Tasks ##
################
#
# uncomment and implement the following functions
# the input is a rule and it is meant to add to facts all new facts derivable from the rule applications
def apply_rule(rule):
    body, head = rule  # Unpack the rule: body (conditions), head (inferred fact)
    substitutions = find_substitutions(body, {}, [])  # Find variable matches
    return derive(substitutions, head)  # Apply and derive new fact


# no input needed as facts and rules are considered global
# the function should cycle through the rules until no new fact can be derived
def saturateKB():
    new_fact_found = True  # Keep iterating while new facts are found
    while new_fact_found:
        new_fact_found = False  # Assume no new facts will be found
        for rule in rules:
            if apply_rule(rule):  # If new facts are inferred
                new_fact_found = True  # Continue iterating
#
# use the functions add_fact and add_rule to test your implementation on the preworkshop exercises
def euclidean_distance(p1,p2,rel):
    a,b = p1
    c,d = p2
    euclidean_distance = numpy.sqrt((a-c)**2 + (b-d)**2)*(1+(int(rel[1])-1)*0.2)
    return euclidean_distance

add_rule(
    [("Node", "Origin"), ("R#", "Origin", "Destination")], 
    ("R#", "Origin", "Destination")
)



add_fact("Node",(0,0))
add_fact("R1",(0,0),(-2,2))
add_fact("R1",(0,0),(2,-1))

add_fact("Node",(-2,2))
add_fact("R2",(-2,2),(-4,0))

add_fact("Node",(-4,0))
add_fact("R4",(-4,0),(0,-4))

add_fact("Node",(0,-4))
add_fact("R1",(0,-4),(4,-2))
add_fact("R2",(0,-4),(0,0))

add_fact("Node",(4,-2))
add_fact("R5",(4,-2),(4,1))

add_fact("Node",(4,1))
add_fact("R4",(4,1),(4,-2))

add_fact("Node",(2,-1))
add_fact("R2",(2,-1),(2,2))
add_fact("R1",(2,-1),(2,2))
add_fact("R5",(2,-1),(0,-4))

add_fact("Node",(2,2))
add_fact("R3",(2,2),(0,0))
add_fact("R2",(2,2),(4,1))

add_fact("A",(4,-2),(2,-1))  


add_fact("B", (0,0), (4,-2))
add_fact("C", (0,0), (4,-2), (2,1), (0,-4))

add_fact("D",(6,5),(6,4))



objective_value= []




def normalize(fact_set): #Made for standarizing all possible inputs to functions
        normalized = set()
        for item in fact_set:
            if isinstance(item, tuple) and len(item) > 1 and isinstance(item[0], tuple):  
                normalized.update(item)  # ✅ Flatten tuple of tuples
            else:
                normalized.add(item)  # ✅ Add normal tuples
        return normalized



def update_goals(objectives):
    
    if objectives[0] not in facts:
        return set()     

    first = normalize(facts[objectives[0]])  

    for i in objectives[1:]:  # ✅ Iterate from the second element onward
        if i in facts:  # ✅ Ensure the fact exists
            first &= normalize(facts[i])  # ✅ Find intersection of normalized sets
        else:
            return set()  # ✅ If any fact is missing, return empty set

    return first
    
    


objective_value = update_goals(["B","A","C"])     
print(objective_value)    
def run(start, costlimit, allowed):
    path_already_done = [] 
    costs = []
    best_paths = []

    connected_facts = set()
    for relation in allowed:
        if relation in facts:
            connected_facts.update(facts[relation]) 

    if not connected_facts:
        return "No valid paths found: No valid connections exist"

    priority_queue = [(0, start, [start])]  
    shortest_distance = {start: 0} 

    while priority_queue:
        cost, current, path = heapq.heappop(priority_queue) 

 
        if cost > costlimit:
            continue

        if current in objective_value and path not in path_already_done:
            print(f"Found path: {path} with cost: {cost}")
            path_already_done.append(path)
            costs.append(cost)

            best_paths.append((cost, path))  
            
   
            if len(best_paths) == 3:
                break  

        for node, neighbor in connected_facts:
            if node == current:
                distance = euclidean_distance(current, neighbor, "R1")  # Assuming "R#" relations exist
                new_cost = cost + distance

               
                if new_cost > costlimit:
                    continue  

            
                if neighbor not in shortest_distance or new_cost < shortest_distance[neighbor]:
                    shortest_distance[neighbor] = new_cost
                    heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))

    
    if best_paths:
        best_paths.sort()  
        return [f"Path {i+1}: {path} with cost: {cost}" for i, (cost, path) in enumerate(best_paths)]
    else:
        return "No valid paths found within cost limit"







print(run((0,0),150, ["R1","R2","R3","R4","R5"] ))
print("NOW SATURATED")
saturateKB()
print(run((0,0),150, ["R1","R2","R3","R4","R5"] ))
#print(facts)
#print(euclidean_distance((2,-1),(0,-4),"R5")+(euclidean_distance((0,0),(2,-1),"R1")))



#print(numpy.sqrt(8))
#print(facts)
#add_fact("B",(-2,2))
#add_fact("C",(2,2))
#add_fact("D",(4,1))
#add_fact("E",(4,-2))
#add_fact("F",(-4,0))
#add_fact("G",(2,-1))
#add_fact("H",(0,-4))
#print(euclidean_distance((1,1),(2,2),"R2"))


