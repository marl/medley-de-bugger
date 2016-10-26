# medley-de-bugger

Hello! MedleyDeBugger is an application that processes and error-checks multitracks before they are uploaded to the MedleyDB database.

*Maintained by:*

Julia Wilkins @jlw365

Rachel Bittner @rabitt


This code is released along with [MedleyDB](http://medleydb.weebly.com) and is a component of the work presented in the following publication:

[R. Bittner](https://github.com/rabitt), [J. Wilkins](https://github.com/jlw365), [H. Yip](https://github.com/hmyip1) and J. P. Bello,
"[MedleyDB 2.0: New Data and a System for Sustainable Data Collection](https://wp.nyu.edu/ismir2016/wp-content/uploads/sites/2294/2016/08/bittner-medleydb.pdf)", in
Proceedings of the 17th International Society for Music Information Retrieval Conference Late Breaking and Demo Papers,
New York City, USA, Aug. 2016.


Related Projects
----------------
MedleyDB [[code repository]](https://github.com/marl/medleydb) [[website]](http://medleydb.weebly.com)

[MedleyDB Manager](https://github.com/marl/medleydb_manager)


Installation (via Homebrew)
---------------------------
- `git clone https://github.com/marl/medley-de-bugger.git`
- `cd medley-de-bugger`
- `pip install -r requirements.txt`
- `brew install sox`
- `brew install qt`
- `brew install sip`
- `brew install pyqt`

Usage
-----
`# launch the application`
`python new_multitrack/new_multitrack.py` 

- Follow the prompts to select your audio and run it through the app.
- After you're done, a new folder will be generated with a multitrack in MedleyDB format.
