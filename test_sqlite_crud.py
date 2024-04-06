from sqlite_crud import DbUser

testData = {
  'name': 'John Doe',
  'email': 'john.doe@example.com',
  'password': 'test123',
  'age': 30,
  'gender': 'M',
  'address': '123 Main St'
}

testData2 = {
  'name': 'Jane Doe',
  'email': 'jane.doe2@example.com',
  'password': '12345',
  'age': 42,
  'gender': 'F',
  'address': '321 Contact St'
}

user = DbUser()

# Create
print("Insert:\n", user.insert(**testData), "\n")
# print("Insert:\n", user.insert(**testData2), "\n")
# Reads
print("Select:\n", user.select(min_age=25, max_age=40, gender='M'), "\n")
# Update
print("Update:\n",  user.update(testData['email'], age=45, address='456 Oak St'), "\n")
# Delete
print("Delete:\n",  user.delete(gender='F'), "\n")