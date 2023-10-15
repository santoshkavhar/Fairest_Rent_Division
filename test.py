from helper import *

def test_for_envy(ass_room_list, ass_renters_list, ass_rents_list, allocation, values):

    rent_dict_renter = {}
    allocation_from_1 = {}
    counter = 0
    for i in ass_room_list:
        # start from 0 the rent_dict_renter
        rent_dict_renter[i-1]=ass_rents_list[counter]
        counter += 1

    for key, value in allocation.items():
        allocation_from_1[key+1]=value+1
    
    # print("Allocation:", allocation_from_1, "\nValues:", values, "\nRents: ", rent_dict_renter)
    for i in ass_renters_list:
        # Since i starts from 1
        i -= 1
        for j in ass_room_list:
            # Since j starts from 1
            j -= 1
            # Round to ROUND decimal places
            if  round(values[i][allocation[i]] - rent_dict_renter[allocation[i]], ROUND) < round(values[i][j] - rent_dict_renter[j], ROUND) :
                set_failure()
                print("Envyness found: " , "\tRenter no. " , i , "Allocated room no. " , allocation[i] ,
                      "\nRenter envies allocation of room no. ", j, ".",
                      "Found utility as " , values[i][allocation[i]] - rent_dict_renter[allocation[i]] ,
                      " which is less than the utility " , values[i][j] - rent_dict_renter[j],
                      "\n", values[i][allocation[i]] , "-", rent_dict_renter[allocation[i]], "<", values[i][j], "-", rent_dict_renter[j] )
                set_normal()