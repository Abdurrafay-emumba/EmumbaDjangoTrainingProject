from django.core.cache import cache

"""
File Purpose: This is a self-made file. The purpose of this file is to standardize the cache validation and invalidation.
Since we need to be very specific with the cache name while validating and invalidating, we will create the functions here
that will do that for us.
"""

def create_cache_key_get_task_status_report(user_id):
    """
    Function Purpose: This function will create a cache key for the task status report.
    :param user_id: The user id for which the cache key is to be created
    :return: The cache key
    """
    return f"user:{user_id}:task_status_report"

def add_cache_get_task_status_report(user_id, data, timeout=60 * 15):
    """
    Function Purpose: This function will add the cache for the task status report.
    :param user_id: The user id for which the cache is to be validated
            data: The data to be cached
            timeout: The timeout for the cache (default is 15 minutes)

    :return: Will return True if the cache is set successfully, otherwise False.
    """
    cache_key = create_cache_key_get_task_status_report(user_id)
    return cache.set(cache_key, data, timeout=timeout)

def get_cache_get_task_status_report(user_id):
    """
    Function Purpose: This function will get the cache for the task status report.
    :param user_id: The user id for which the cache is to be validated
    :return: Will return the cached data if it exists, otherwise None.
    """
    cache_key = create_cache_key_get_task_status_report(user_id)
    return cache.get(cache_key)

def invalidate_cache_get_task_status_report(user_id):
    """
    Function Purpose: This function will invalidate the cache for the task status report.
    :param user_id: The user id for which the cache is to be invalidated
    :return: Will return True if the cache is invalidated successfully, otherwise False.
    """
    cache_key = create_cache_key_get_task_status_report(user_id)
    return cache.delete(cache_key)

def create_cache_key_get_average_task_per_day(user_id):
    """
    Function Purpose: This function will create a cache key for the average task per day.
    :param user_id: The user id for which the cache key is to be created
    :return: The cache key
    """
    return f"user:{user_id}:avg_tasks_per_day"

def add_cache_get_average_task_per_day(user_id, data, timeout=60 * 15):
    """
    Function Purpose: This function will add the cache for the average task per day.
    :param user_id: The user id for which the cache is to be validated
            data: The data to be cached
            timeout: The timeout for the cache (default is 15 minutes)

    :return: Will return True if the cache is set successfully, otherwise False.
    """
    cache_key = create_cache_key_get_average_task_per_day(user_id)
    return cache.set(cache_key, data, timeout=timeout)

def get_cache_get_average_task_per_day(user_id):
    """
    Function Purpose: This function will get the cache for the average task per day.
    :param user_id: The user id for which the cache is to be validated
    :return: Will return the cached data if it exists, otherwise None.
    """
    cache_key = create_cache_key_get_average_task_per_day(user_id)
    return cache.get(cache_key)

def invalidate_cache_get_average_task_per_day(user_id):
    """
    Function Purpose: This function will invalidate the cache for the average task per day.
    :param user_id: The user id for which the cache is to be invalidated
    :return: Will return True if the cache is invalidated successfully, otherwise False.
    """
    cache_key = create_cache_key_get_average_task_per_day(user_id)
    return cache.delete(cache_key)

def create_cache_key_get_late_task_report(user_id):
    """
    Function Purpose: This function will create a cache key for the late task report.
    :param user_id: The user id for which the cache key is to be created
    :return: The cache key
    """
    return f"user:{user_id}:late_task_report"

def add_cache_get_late_task_report(user_id, data, timeout=60 * 15):
    """
    Function Purpose: This function will add the cache for the late task report.
    :param user_id: The user id for which the cache is to be validated
            data: The data to be cached
            timeout: The timeout for the cache (default is 15 minutes)

    :return: Will return True if the cache is set successfully, otherwise False.
    """
    cache_key = create_cache_key_get_late_task_report(user_id)
    return cache.set(cache_key, data, timeout=timeout)

def get_cache_get_late_task_report(user_id):
    """
    Function Purpose: This function will get the cache for the late task report.
    :param user_id: The user id for which the cache is to be validated
    :return: Will return the cached data if it exists, otherwise None.
    """
    cache_key = create_cache_key_get_late_task_report(user_id)
    return cache.get(cache_key)

def invalidate_cache_get_late_task_report(user_id):
    """
    Function Purpose: This function will invalidate the cache for the late task report.
    :param user_id: The user id for which the cache is to be invalidated
    :return: Will return True if the cache is invalidated successfully, otherwise False.
    """
    cache_key = create_cache_key_get_late_task_report(user_id)
    return cache.delete(cache_key)

def create_cache_key_get_day_on_which_max_number_of_task_completed(user_id):
    """
    Function Purpose: This function will create a cache key for the day on which max number of task completed.
    :param user_id: The user id for which the cache key is to be created
    :return: The cache key
    """
    return f"user:{user_id}:day_max_tasks_completed"

def add_cache_get_day_on_which_max_number_of_task_completed(user_id, data, timeout=60 * 15):
    """
    Function Purpose: This function will add the cache for the day on which max number of task completed.
    :param user_id: The user id for which the cache is to be validated
            data: The data to be cached
            timeout: The timeout for the cache (default is 15 minutes)

    :return: Will return True if the cache is set successfully, otherwise False.
    """
    cache_key = create_cache_key_get_day_on_which_max_number_of_task_completed(user_id)
    return cache.set(cache_key, data, timeout=timeout)

def get_cache_get_day_on_which_max_number_of_task_completed(user_id):
    """
    Function Purpose: This function will get the cache for the day on which max number of task completed.
    :param user_id: The user id for which the cache is to be validated
    :return: Will return the cached data if it exists, otherwise None.
    """
    cache_key = create_cache_key_get_day_on_which_max_number_of_task_completed(user_id)
    return cache.get(cache_key)

def invalidate_cache_get_day_on_which_max_number_of_task_completed(user_id):
    """
    Function Purpose: This function will invalidate the cache for the day on which max number of task completed.
    :param user_id: The user id for which the cache is to be invalidated
    :return: Will return True if the cache is invalidated successfully, otherwise False.
    """
    cache_key = create_cache_key_get_day_on_which_max_number_of_task_completed(user_id)
    return cache.delete(cache_key)

def create_cache_key_get_number_of_task_opened_every_day(user_id):
    """
    Function Purpose: This function will create a cache key for the number of task opened every day.
    :param user_id: The user id for which the cache key is to be created
    :return: The cache key
    """
    return f"user:{user_id}:number_of_tasks_opened_every_day"

def add_cache_get_number_of_task_opened_every_day(user_id, data, timeout=60 * 15):
    """
    Function Purpose: This function will add the cache for the number of task opened every day.
    :param user_id: The user id for which the cache is to be validated
            data: The data to be cached
            timeout: The timeout for the cache (default is 15 minutes)

    :return: Will return True if the cache is set successfully, otherwise False.
    """
    cache_key = create_cache_key_get_number_of_task_opened_every_day(user_id)
    return cache.set(cache_key, data, timeout=timeout)

def get_cache_get_number_of_task_opened_every_day(user_id):
    """
    Function Purpose: This function will get the cache for the number of task opened every day.
    :param user_id: The user id for which the cache is to be validated
    :return: Will return the cached data if it exists, otherwise None.
    """
    cache_key = create_cache_key_get_number_of_task_opened_every_day(user_id)
    return cache.get(cache_key)

def invalidate_cache_get_number_of_task_opened_every_day(user_id):
    """
    Function Purpose: This function will invalidate the cache for the number of task opened every day.
    :param user_id: The user id for which the cache is to be invalidated
    :return: Will return True if the cache is invalidated successfully, otherwise False.
    """
    cache_key = create_cache_key_get_number_of_task_opened_every_day(user_id)
    return cache.delete(cache_key)

def create_cache_key_get_number_of_task_opened_every_day2(user_id):
    """
    Function Purpose: This function will create a cache key for the number of task opened every day2.
    :param user_id: The user id for which the cache key is to be created
    :return: The cache key
    """
    return f"user:{user_id}:number_of_tasks_opened_every_day2"

def add_cache_get_number_of_task_opened_every_day2(user_id, data, timeout=60 * 15):
    """
    Function Purpose: This function will add the cache for the number of task opened every day2.
    :param user_id: The user id for which the cache is to be validated
            data: The data to be cached
            timeout: The timeout for the cache (default is 15 minutes)

    :return: Will return True if the cache is set successfully, otherwise False.
    """
    cache_key = create_cache_key_get_number_of_task_opened_every_day2(user_id)
    return cache.set(cache_key, data, timeout=timeout)

def get_cache_get_number_of_task_opened_every_day2(user_id):
    """
    Function Purpose: This function will get the cache for the number of task opened every day2.
    :param user_id: The user id for which the cache is to be validated
    :return: Will return the cached data if it exists, otherwise None.
    """
    cache_key = create_cache_key_get_number_of_task_opened_every_day2(user_id)
    return cache.get(cache_key)

def invalidate_cache_get_number_of_task_opened_every_day2(user_id):
    """
    Function Purpose: This function will invalidate the cache for the number of task opened every day2.
    :param user_id: The user id for which the cache is to be invalidated
    :return: Will return True if the cache is invalidated successfully, otherwise False.
    """
    cache_key = create_cache_key_get_number_of_task_opened_every_day2(user_id)
    return cache.delete(cache_key)




