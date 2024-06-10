def Commonfields():
    dic={
         'job_title':[],
         'job_link':[],
         'vendor':[],
         'job_experience':[],
         'job_location':[],
         'posted_on':[],
         'job_description':[],
         'job_country':[],
         'job_salary':[],
         'job_short_description':[],
         'job_industry':[],
         'Employment_type':[],
         'job_skills':[],
         'positions':[],
         'job_source':[],
         'email':[],
         'phone':[],
         'category_skill':[],
         'extracted_date': [],
         'remarks': [],
         'source': [],
         'isexist':0,
         'received_from':[],
         'vendor_type':[],
         'job_status':[]
        }
    return(dic)


# # Update Commonfields function to accept a list of keys
# def Commonfields(keys):
#     # Initialize an empty dictionary
#     dic = {}
    
#     # Add keys to the dictionary with empty lists as values
#     for key in keys:
#         dic[key] = []
    
#     # Add additional keys specific to your data
#     dic.update({
#         'source': '',
#         'isexist': 0
#     })
    
#     return dic