import pickle
# from vk_api_local import vk1, vk2, vk3, vk4, vk5
import threading


# should be executed before everything else
def extract_ids():
    with open("all_students_raw.pickle", "rb") as f:
        students_nogroups = pickle.load(f)

    ids = []
    for i in students_nogroups:
        key = list(i.keys())[0]
        students_list = i[key]["students"]
        for student in students_list:
            stid = student["id"]
            ids.append(stid)
    with open("student_ids_list.pickle", "wb") as f1:
        pickle.dump(ids, f1)


class FriendsThread(threading.Thread):
    friends = dict()

    def __init__(self, ids, vk_local):
        threading.Thread.__init__(self)
        self.ids = ids
        self.vk_local = vk_local

    def run(self):
        code_to_join = []
        tag = []
        for i in enumerate(self.ids):
            code_to_join.append(
                "var a%i = API.friends.get({'user_id': %i, 'offset': 0, 'fields': 'name'});" % (i[0], i[1]))
            tag.append("a%i" % i[0])
        first_part = " ".join(code_to_join)
        tag = ", ".join(tag)
        final_code = first_part + " return [" + tag + "];"

        response = self.vk_local.execute(code=final_code)

        # iterate over the response
        for i, resp in enumerate(response):
            current_id = self.ids[i]

            if resp is False:  # friend list can't be accessed
                FriendsThread.friends.update({current_id: False})
            else:
                FriendsThread.friends.update({current_id: {"count": resp['count'],
                                                           "friends": resp['items']}})

def inf_loop(list_):
    while True:
        for i in list_:
            yield i

def get_friendlist():
    with open("student_ids_list.pickle", "rb") as stids_f:
        all_ids = pickle.load(stids_f)

    threads = []
    vks = [vk1, vk2, vk3, vk4, vk5]
    cycle_vk = inf_loop(vks)  # to use different tokens one after another
    temp_ids = []
    iter = 1

    used = []


    for uid in all_ids:
        if len(temp_ids) < 22:
            temp_ids.append(uid)
            used.append(uid)
        else:
            temp_ids.append(uid)
            used.append(uid)
            temp_thread = FriendsThread(ids=temp_ids, vk_local=next(cycle_vk))
            threads.append(temp_thread)
            temp_thread.start()
            for j in threads:
                j.join()
            temp_ids.clear()
            print(f'done {iter}')
            iter += 1

    if temp_ids:
        print(len(temp_ids))
        temp_thread = FriendsThread(ids=temp_ids, vk_local=next(cycle_vk))
        threads.append(temp_thread)
        temp_thread.start()
        temp_thread.join()

    friends = FriendsThread.friends
    with open("friends_only.pickle", "wb") as f2:
        pickle.dump(friends, f2)

# as a result, we have a list of each student's friends


with open("all_students_raw.pickle", "rb") as f:
    print(pickle.load(f)[0])