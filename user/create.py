# user/create.py
# -----------------
# Definition of functions for create users for our Junior DBA
#

def create_user(session=None):
    # Get hold of the global shell object
    import mysqlsh
    shell = mysqlsh.globals.shell

    if session is None:
        session = shell.get_session()
        if session is None:
            print("No session specified. Either pass a session object to this "
                  "function or connect the shell to a database")
            return

    user_login = shell.prompt("Enter the new user's account: ")
    user_password = shell.prompt('Enter the password (leave is blank to generate one): ',{'type': 'password'})
    user_reset = shell.prompt('Does the user need to change his password ? (Y,n) ', {'defaultValue': 'y'})    
    user_failed = shell.prompt('Do you want to lock the account after 3 failed attempts ? (Y,n) ', {'defaultValue': 'y'})

    stmt="CREATE USER {} IDENTIFIED BY ".format(user_login)
    if user_password == "":
        stmt = stmt + "RANDOM PASSWORD "
    else:
        stmt = stmt + "'{}' ".format(user_password)
    if user_reset.upper() == "Y":
        stmt = stmt + "PASSWORD EXPIRE "
    if user_failed.upper() == "Y":
        stmt = stmt + "FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 2"
        
    # just for DEBUG ;-)    
    print("DEBUG: {}".format(stmt))       
    
    result = session.run_sql(stmt)
    shell.dump_rows(result)

    return