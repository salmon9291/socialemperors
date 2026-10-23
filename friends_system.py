import logging
from sessions import session, save_session, get_target_session, save_target_session, SESSION_SAVE

log = logging.getLogger('__main__')

def initialize_friends_list(save):
    if "friends" not in save["privateState"]:
        save["privateState"]["friends"] = []
    if "friendRequests" not in save["privateState"]:
        save["privateState"]["friendRequests"] = []
    return save

def add_friend(userid, friend_userid):
    save = session(userid)
    friend_save = get_target_session(friend_userid)

    if not save or not friend_save:
        return False

    save = initialize_friends_list(save)
    friend_save = initialize_friends_list(friend_save)

    if friend_userid in save["privateState"]["friends"]:
        return False

    save["privateState"]["friends"].append(friend_userid)
    friend_save["privateState"]["friends"].append(userid)

    if friend_userid in save["privateState"]["friendRequests"]:
        save["privateState"]["friendRequests"].remove(friend_userid)
    if userid in friend_save["privateState"]["friendRequests"]:
        friend_save["privateState"]["friendRequests"].remove(userid)

    save_session(userid, False)
    save_target_session(friend_userid, friend_save, SESSION_SAVE)
    return True

def remove_friend(userid, friend_userid):
    save = session(userid)
    friend_save = get_target_session(friend_userid)

    if not save or not friend_save:
        return False

    save = initialize_friends_list(save)
    friend_save = initialize_friends_list(friend_save)

    if friend_userid not in save["privateState"]["friends"]:
        return False

    save["privateState"]["friends"].remove(friend_userid)
    if userid in friend_save["privateState"]["friends"]:
        friend_save["privateState"]["friends"].remove(userid)

    save_session(userid, False)
    save_target_session(friend_userid, friend_save, SESSION_SAVE)
    return True

def send_friend_request(userid, target_userid):
    save = session(userid)
    target_save = get_target_session(target_userid)

    if not save or not target_save:
        return False

    save = initialize_friends_list(save)
    target_save = initialize_friends_list(target_save)

    if userid == target_userid:
        return False
    if target_userid in save["privateState"]["friends"]:
        return False
    if userid in target_save["privateState"]["friendRequests"]:
        return False

    target_save["privateState"]["friendRequests"].append(userid)
    save_target_session(target_userid, target_save, SESSION_SAVE)
    return True

def accept_friend_request(userid, requester_userid):
    save = session(userid)
    requester_save = get_target_session(requester_userid)

    if not save or not requester_save:
        return False

    save = initialize_friends_list(save)
    requester_save = initialize_friends_list(requester_save)

    if requester_userid not in save["privateState"]["friendRequests"]:
        return False

    save["privateState"]["friendRequests"].remove(requester_userid)

    if requester_userid not in save["privateState"]["friends"]:
        save["privateState"]["friends"].append(requester_userid)
    if userid not in requester_save["privateState"]["friends"]:
        requester_save["privateState"]["friends"].append(userid)

    save_session(userid, False)
    save_target_session(requester_userid, requester_save, SESSION_SAVE)
    return True

def reject_friend_request(userid, requester_userid):
    save = session(userid)
    if not save:
        return False

    save = initialize_friends_list(save)

    if requester_userid not in save["privateState"]["friendRequests"]:
        return False

    save["privateState"]["friendRequests"].remove(requester_userid)
    save_session(userid, False)
    return True

def get_friends_list(userid):
    save = session(userid)
    if not save:
        return []
    save = initialize_friends_list(save)
    return save["privateState"]["friends"]

def get_friend_requests(userid):
    save = session(userid)
    if not save:
        return []
    save = initialize_friends_list(save)
    return save["privateState"]["friendRequests"]

def is_friend(userid, target_userid):
    return target_userid in get_friends_list(userid)

def get_friends_info(userid):
    from sessions import fb_friend_info
    friends = []
    for friend_id in get_friends_list(userid):
        friend_save = get_target_session(friend_id)
        if friend_save:
            friends.append(fb_friend_info(friend_save["playerInfo"]))
    return friends
