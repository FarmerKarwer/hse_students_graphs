from vk_api import VkApi

session1 = VkApi('login', 'password')
session1.auth()
vk1 = session1.get_api()

session2 = VkApi('login', 'password')
session2.auth()
vk2 = session1.get_api()

session3 = VkApi('login', 'password')
session3.auth()
vk3 = session1.get_api()

session4 = VkApi('login', 'password')
session4.auth()
vk4 = session1.get_api()

session5 = VkApi('login', 'password')
session5.auth()
vk5 = session1.get_api()
