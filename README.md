# RePlace
Placement Portal IITB
### How to run?
Run the following commands in the same directory as the fetched repo.
```
source env/bin/activate
pip3 install -r requirements.txt
python src/manage.py runserver
```
Open [127.0.0.1:8000](http://127.0.0.1:8000/) to get to the home page of **RePlace**.

 
### Status 
- Login pages for company, student and coordinator combined
- Logout created
- All static files in one place
- Show basic jaf information 
- Parallax in home page
- Home page scroll animation
- Error display mechanism on login pages

- Models created (may be few changes in future) (signing deadline not part of jaf_test) MEET
- Parallax improving LATER

#### Company
- Company registration form created 
- Jaf creation form almost complete (Not all combinations taken care of in the jaf creation form) MEET
- Post company jaf form (not yet started) DEPAL

#### IC
- IC tabs for resume selection status (resume verification post pending) SOURABH
- Make resume upload, view (testing remaining) DEPAL
- Update​ database​ regarding​ ​test​​ location,​​ timing​ ​and​​ other​ updates (css done backend remaining) DEPAL

#### Student
- Student Home page done
- Provide​ ​ reviews​ ​ for​ ​ completed​ ​ internships
- Filters for students (not much done... in progress) MEET
- Make sign jaf view (not yet started) DEPAL

### Plans 
- Login​ ​ and​ ​ Logout​ ​ for​ ​ all​ ​ users (DONE)

#### Admin
- Initially​ ​ populate​ ​ the​ ​ database (rish)
- Update​ ​ database​ ​ at​ ​ end​ ​ of​ ​ the​ ​ semester/year​ ​ regarding​ ​ new​ ​ admissions,​ ​ CPI change​ ​ etc,.​ ​ (if​ ​ time​ ​ permits)
- This​ ​ part​ ​ represents​ ​ the​ ​ connections​ ​ of​ ​ our​ ​ project​ ​ with​ ​ rest​ ​ of​ ​ database​ ​ tables​ ​ in the​ ​ university

#### Student
- View​ ​ and​ ​ Sign​ ​ eligible​ ​ JAFs (PARTIAL)
- Provide​ ​ reviews​ ​ for​ ​ completed​ ​ internships (DONE)
- Search​ ​ current​ ​ JAFs​ ​ according​ ​ to​ ​ various​ ​ filters (PARTIAL)
- View​ ​ all​ ​ data​ ​ regarding​ ​ past​ ​ interns​ ​ including​ ​ reviews,​ ​ selections​ ​ and​ ​ procedures (RISH)
- Upload​ ​ resume​ ​ and​ ​ see​ ​ status​ ​ of​ ​ verification​ (if​ ​ time​ ​ permits) (PARTIAL)
- Confirm​ ​ final​ ​ selection​ ​ for​ ​ students​ ​ finally​ ​ shortlisted​ ​ by​ ​ companies (CANCEL)


#### IC
- Verify​ ​ resumes (PARTIAL)
- Update​ database​ ​ regarding​ ​ test​ ​ location,​ ​ timing​ ​ and​ ​ other​ ​ updates (PARTIAL)

#### Company
- Create​ ​ JAFs​ ​ and​ ​ see​ ​ specific​ ​ resume​ ​ number​ ​ of​ ​ applicants (PARTIAL)
- Set​ ​ eligibility​ ​ conditions (PARTIAL)
- Shortlist​ ​ based​ ​ on​ ​ the​ ​ resumes​ ​ of​ ​ applicants (SOURABH)
- See​ ​ progress​ ​ level​ ​ of​ ​ shortlisted​ ​ students​ ​ according​ ​ to​ ​ various​ ​ sequential​ ​ tests​ ( ​if time​ ​ permits) (NOPE)
- Give​ ​ final​ ​ selections​ ​ and​ ​ see​ ​ the​ ​ confirmation​ ​ status​ ​ by​ ​ selected​ ​ students. (SOURABH)


### Filers 

#### Done
- Company category
- Signed, Unsigned
- CPI (later) (range)
- Stipend (range)
- Can sign
- Job Profile
- Pre deadline

#### ToDo