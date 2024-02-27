from email_validator import validate_email, EmailNotValidError
class Validation:
    def valid_email(email_):
        try:
            valid = validate_email(email_)
            email_ = valid.email
            return True
        except EmailNotValidError as e:
            print(e)
            return False
    def password_confirmation(pswrd, confirm_pswrd):
        if pswrd == confirm_pswrd:
            return True
        return False
    def email_confirmation(email_, confirm_email):
        if email_ == confirm_email:
            return True
        return False
