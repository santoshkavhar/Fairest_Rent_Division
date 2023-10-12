
def test_for_envy(ass_room_list, ass_renters_list, ass_rents_list, allocation, values):
    # agent_dict = {v: k for v, k in enumerate(ass_renters_list)}
    # room_dict = {v: k for v, k in enumerate(ass_room_list)}
    rent_dict_renter = {str(v+1): k for v, k in enumerate(ass_rents_list)}
    rent_dict_room = {}
    counter = 0
    for i in ass_room_list:
        rent_dict_renter[i]=ass_rents_list[counter]
        counter += 1
    # rent_dict_renter = {str(v+1): k for v, k in enumerate(ass_rents_list)}
    
    print("Allocation:", allocation, "\nValues:", values, "\nRents: ", rent_dict_renter)
    for i in ass_renters_list:
        for j in ass_room_list:
            if  values[i][allocation[i]] - rent_dict_renter[allocation[i]] < values[i][j] - rent_dict_renter[j] :
                print("Envyness found: " , "\tRenter no. " , i , "Allocated room no. " , allocation[i] ,
                      "\nRenter envies allocation of room no. ", j, ".",
                      "Found utility as " , values[i][allocation[i]] - rent_dict_renter[i] ,
                      " which is less than the utility " , values[i][j] - rent_dict_renter[j],
                      "\n", values[i][allocation[i]] , "-", rent_dict_renter[allocation[i]], "<", values[i][j], "-", rent_dict_renter[j] )