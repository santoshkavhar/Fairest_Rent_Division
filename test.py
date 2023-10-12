
def test_for_envy(ass_room_list, ass_renters_list, ass_rents_list, allocation, values):

    rent_dict_renter = {}
    counter = 0
    for i in ass_room_list:
        rent_dict_renter[i]=ass_rents_list[counter]
        counter += 1
    
    print("Allocation:", allocation, "\nValues:", values, "\nRents: ", rent_dict_renter)
    for i in ass_renters_list:
        for j in ass_room_list:
            if  values[i][allocation[i]] - rent_dict_renter[allocation[i]] < values[i][j] - rent_dict_renter[j] :
                print("Envyness found: " , "\tRenter no. " , i , "Allocated room no. " , allocation[i] ,
                      "\nRenter envies allocation of room no. ", j, ".",
                      "Found utility as " , values[i][allocation[i]] - rent_dict_renter[i] ,
                      " which is less than the utility " , values[i][j] - rent_dict_renter[j],
                      "\n", values[i][allocation[i]] , "-", rent_dict_renter[allocation[i]], "<", values[i][j], "-", rent_dict_renter[j] )