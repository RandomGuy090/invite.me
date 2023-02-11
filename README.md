invite.me
===

# What is it?
Invite.me is webapp created for my prom night. We needed a software able to create and send invitations, and gather the feedback from participants.

# How does it work?
I have wrote it with python's Flask framework. Because it became a little "too big" than I expected I have used blueprints for easier maintain. Project has MVC-based architecture, with two "REST" endpoints. REST is in quotes because it has only one common feature - using JSON (xD). 

# First apperance
## Set program up
To launch our lovely app you have to have smtp email (or smtp relay). Add credentials to the src/config.py (WIP to add env variables). Edit also ``app.config['APPLICATION_ROOT']`` variable. Insert there you URL root domain. In my case it will look like below:
```python
app.config['APPLICATION_ROOT'] = 'http://172.24.117.120:5000/'
```

After that we can run app with:
```bash
flask --app invite_me  --debug run --host=0.0.0.0
```
![image](https://user-images.githubusercontent.com/64653975/217215519-977254bb-9061-43c5-9fe0-9cc3314412ad.png)

Register with your real email address.
![image](https://user-images.githubusercontent.com/64653975/217216078-b641357d-288e-49bb-83ab-aa84489ed5d0.png)
and you will be redirected to authentication site

![image](https://user-images.githubusercontent.com/64653975/218274067-6355aec8-fb97-438a-b6c5-39749c667905.png)


on your email inbox you will have got activation link. Click on it
![image](https://user-images.githubusercontent.com/64653975/217488713-210628fa-10fe-423c-a27c-ea1beef7b549.png)

...and you can go on main page of system

![image](https://user-images.githubusercontent.com/64653975/217489495-6923e97e-1a1a-4ead-9538-f019025f103d.png)

![image](https://user-images.githubusercontent.com/64653975/217489601-9c082b74-a7bf-4c0b-83a2-192a6424a8d7.png)

## Adding new event
Let's say I became a President of The United States and I'm about to throw some party.
![image](https://user-images.githubusercontent.com/64653975/218272345-c4821653-0529-4d3e-b957-bb57a199e02a.png)

I have fulfilled creating event form:
	- event name -> name of an event
	- event date -> date of an event
	- delcaration deadline -> deadline for sending delcaration
	- event address -> address of the event place
	- image link in header -> link to the image placed in header
	- image link in footer ->  link to the image placed in footer
	- google map link -> google map link
	- place img -> image of the place where event will happen
	- declaration email content -> content of declaration
	- invitation email content -> content of invitaiton
	- contact to the organizators -> contact to the organizators of en event

![image](https://user-images.githubusercontent.com/64653975/218272567-1449cdaa-c8d9-49e8-8e7a-e769a99b5ca2.png)

Event will be added after you click "submit" button. In table header we have mostly same information which I written a minute ago, while adding. But you can find some new collumns and buttons:
	- remove -> button to remove event
	- update event -> button redirects to the event edit page
	- send ->
		- send delcaration -> send delcaration to all users added to this event
		- send invitation -> send invitation to all users added to this event
	- event view -> all users and divisions added to this event

## Edit events
After clicking ``update_event`` on main page you will be redirected to editing page
![screencapture-172-24-117-120-5000-event-update-2023-02-11-19_14_18](https://user-images.githubusercontent.com/64653975/218274485-86ec378e-0604-482c-aa0a-d0eba2abf30c.png)

Screen above is result of data which I entered while creating event. On the left side is visualised Invitation, declaration is on the right.
All personal data of participant are preparated, so qrcode is invalid. Names and email of participants are >John and Jane Doe.
Let's change declaration content. I will add name and address. I can easily use variables in jinja2 way
to add address I'll add ``{{ participant.event_address }}`` and click button.
After clicking page should refresh and declaration will be updated.

![image](https://user-images.githubusercontent.com/64653975/218275721-39f68cde-a32c-4c2f-8606-762e88f00799.png)

Let's change header image on something better than my githun profile picture. I'll add The White House emblem found on the internet.
![the_white_house.png](https://www.whitehouse.gov/wp-content/uploads/2021/01/cropped-cropped-wh_favicon.png)
![image](https://user-images.githubusercontent.com/64653975/218275812-7e663d77-5fdf-4327-ba5b-fb4387ef2cfe.png)



![image](https://user-images.githubusercontent.com/64653975/218275953-6b997b4a-9567-4d5a-ad60-39d848477182.png)

And database is up to date.

## Adding participants

### Divisions
To add participants we have to add divisions. Divisions are easy way to manage users. Let's go back to homepage and add first division in ``add divisons`` section.
First division I'll name ``friends`` and their supervisor will be ``administrator``.
![image](https://user-images.githubusercontent.com/64653975/218276150-7ecb328e-5792-496b-af3d-8bb63717e6a3.png)



![image](https://user-images.githubusercontent.com/64653975/218276161-964f1d75-cba2-439e-a223-40b32600ac1f.png)

Same as in events secition, after adding division will appear table showing all divisions. ``group view`` button will redirect us to the page with filtered users attached to this division and event.


## Participants

With first divison we can easily add new participant. In the ``add participants`` section  we need to fulfill form.
In form only email is required, so let's start with this singular field.
![image](https://user-images.githubusercontent.com/64653975/218276378-62053562-d671-42fc-8357-5c662ac06017.png)
Pay attention to the ``division`` and ``event`` dropdown inputs.

![image](https://user-images.githubusercontent.com/64653975/218276487-788a1475-bfb7-4e8a-b35e-0053799c60c5.png)

Two green fields on right side informs state of email. Green means unsend, red - already sent. User has neither first nor last name so I'll send declaration to gather data.
![image](https://user-images.githubusercontent.com/64653975/218276540-850a5853-134e-41f6-b5db-77835fc93cbe.png)

how does declaration look on Gmail:
![image](https://user-images.githubusercontent.com/64653975/218276827-cc5ab344-aa2b-4db7-ba9e-6c20c0b9c2bf.png)
As you can see, all updates were sent.

declaration: ![image](https://user-images.githubusercontent.com/64653975/218276970-92c086f2-5376-4024-b13d-5352b046cacc.png)

Let's fill first and last name.
![image](https://user-images.githubusercontent.com/64653975/218277035-ca7cdc06-7549-4aa4-abfd-5e30281ec783.png)
After clicking `Send declaration` button form will be send and participant will be redirected to the above page.
Data are udpated so administrator will see change.
![image](https://user-images.githubusercontent.com/64653975/218277107-54d162fe-e6a0-4864-99a1-6eb6fc304f1f.png)

First and Last name will be changed as well as ``declarated`` flag will turn green.
Participant can still update data, or event cancel.
Update:
![image](https://user-images.githubusercontent.com/64653975/218277188-05233d48-a07e-4311-9de7-43bba9869733.png)

Cancellation:
![image](https://user-images.githubusercontent.com/64653975/218277212-4799101c-2448-4aa3-99b2-b5248f6a65ca.png)

![image](https://user-images.githubusercontent.com/64653975/218277226-7d924bdb-7790-4301-957f-3511e7806d40.png)

All actions can be performed by administrator by joining to the declaration with ``go to declaration`` and ``cancel`` or ``uncancel`` buttons.
Let's uncancel and send invitaiton.

![image](https://user-images.githubusercontent.com/64653975/218277309-d461a116-4f18-49b1-84b2-5e3e59ed030a.png)

invitation on Gmail:
![image](https://user-images.githubusercontent.com/64653975/218278121-755bb05b-6d87-4927-aaf4-0367516b38e5.png)
![image](https://user-images.githubusercontent.com/64653975/218278131-db3a0000-1a82-453e-a5ac-f3dcb8bf9fc8.png)
![image](https://user-images.githubusercontent.com/64653975/218278143-d78933ad-00d1-48d7-a07f-2259ccf45e23.png)

Invitation link below or clicking on QR codes will redirect participant to the electronic version of invitation.
![image](https://user-images.githubusercontent.com/64653975/218278509-a31a2ed3-8be7-4e91-bf30-2b65f47ba552.png)

Administrator opening invitation will register acitivity.
![image](https://user-images.githubusercontent.com/64653975/218278561-5fe86930-af6d-495e-a5dc-62aeb590acbc.png)

![image](https://user-images.githubusercontent.com/64653975/218278576-2f2af0d8-eb4a-4b7a-a7e4-932032cca1eb.png)
When admin opens url for the first time, app will register as getting into an event. Every other opening will be inverting status of participant.

### Multiple participants
It is avaliable to add participants with csv file

what do you need to create import file?
Most important fields are:  ``email`` and ``division``. ``divison`` field can be defined in dropdown input in adminpanel so the easiest way to create file is below.

```
email
import1@user
import2@user
import3@user
import4@user
import5@user
import6@user
import7@user
```

remember to change division

![image](https://user-images.githubusercontent.com/64653975/218278974-6dc47dcf-1193-465d-8b8b-a8149b107e63.png)


![image](https://user-images.githubusercontent.com/64653975/218279726-039335b6-f802-45ad-a1d2-6fd59a08d0c9.png)

``first_name`` and ``last_name`` are optional fields.
Administrator doesn't have to create divisons by hand, he can easily add ``divison`` and ``division_leader`` collumn to the csv file.
```
email,first_name,last_name,division,division_leader
import1@user,import1_name,import1_last,1_division,1_division_leader
import2@user,import2_name,import2_last,2_division,2_division_leader
import3@user,import3_name,import3_last,3_division,3_division_leader
import4@user,import4_name,import4_last,4_division,4_division_leader
import5@user,import5_name,import5_last,5_division,5_division_leader
import6@user,import6_name,import6_last,6_division,6_division_leader
import7@user,import7_name,import7_last,7_division,7_division_leader
```
![image](https://user-images.githubusercontent.com/64653975/218280002-01387f91-9a27-4595-8119-7eb60599f5fc.png)

