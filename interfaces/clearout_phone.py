# default imports
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
import requests
import os

# base directories
ROOT_DIRECTORY = os.getcwd()
APPLICATION_DATA = os.path.join(ROOT_DIRECTORY, "application_data")


class ClearoutPhone(QWidget):
    def __init__(self):
        super(ClearoutPhone, self).__init__()

        # global attributes
        self.heading_font = QFont("Poppins", 18)
        self.heading_font.setBold(True)
        self.heading_font.setWordSpacing(2)
        self.heading_font.setLetterSpacing(QFont.AbsoluteSpacing, 1)

        self.secondary_heading_font = QFont("Poppins", 16)
        self.secondary_heading_font.setWordSpacing(2)
        self.secondary_heading_font.setLetterSpacing(QFont.AbsoluteSpacing, 1)

        self.paragraph_font = QFont("Poppins", 13)
        self.paragraph_font.setWordSpacing(2)
        self.paragraph_font.setLetterSpacing(QFont.AbsoluteSpacing, 1)

        self.screen_size = QApplication.primaryScreen().availableSize()
        self.clearout_phone_window_width = self.screen_size.width() // 2.7
        self.clearout_phone_window_height = self.screen_size.height() // 2

        self.numbers_file_location = None
        self.cleaned_emails = ["abc1@gmail.com", "abc2@gmail.com", "abc3@gmail.com", "abc4@gmail.com"]
        self.clearout_phone_api = "https://api.clearoutphone.io/v1/phonenumber/validate"

        # instance methods
        self.window_configurations()
        self.user_interface()

    def window_configurations(self):
        self.setFixedWidth(int(self.clearout_phone_window_width))
        self.setFixedHeight(int(self.clearout_phone_window_height))
        self.setWindowTitle("Clearout Phone")

    def user_interface(self):
        # master layouts
        self.master_layout = QVBoxLayout()
        self.master_layout.setContentsMargins(45, 50, 45, 20)
        self.header_layout = QVBoxLayout()
        self.body_layout = QVBoxLayout()
        self.child_numbers_layout = QHBoxLayout()
        self.footer_layout = QHBoxLayout()

        # widgets
        self.welcome_label = QLabel()
        self.welcome_label.setFont(self.heading_font)
        self.welcome_label.setText("Welcome to Clearout Phone ")

        self.modules_and_libraries_used_label = QLabel()
        self.modules_and_libraries_used_label.setFont(self.secondary_heading_font)
        self.modules_and_libraries_used_label.setText("PyQt5 | OpenPyXL | Requests")

        self.clearout_phone_fields_label = QLabel()
        self.clearout_phone_fields_label.setFont(self.paragraph_font)
        self.clearout_phone_fields_label.setText("Clearout Phone Fields : ")

        self.clearout_phone_fields_groupbox = QGroupBox()
        self.clearout_phone_fields_groupbox.setFlat(True)
        self.clearout_phone_fields_groupbox.setContentsMargins(10, 10, 10, 10)
        self.clearout_phone_fields_groupbox.setStyleSheet("""QGroupBox{background-color: transparent; 
        border: 2px solid silver; border-radius: 10px;}""")

        self.numbers_label = QLabel()
        self.numbers_label.setFont(self.paragraph_font)
        self.numbers_label.setText("Numbers : ")

        self.get_numbers_file_location = QLineEdit()
        self.get_numbers_file_location.setFont(self.paragraph_font)
        self.get_numbers_file_location.setPlaceholderText("choose .txt file ...")
        self.get_numbers_file_location.setReadOnly(True)
        self.get_numbers_file_location.setFixedSize(int(self.width() // 2.1), int(self.height() // 12))
        self.get_numbers_file_location.setStyleSheet("""QLineEdit{border: 0px; border-radius: 15px; padding-left:10px; 
        padding-right: 10px;}""")

        self.browse_numbers_file_button = QPushButton()
        self.browse_numbers_file_button.setFont(self.paragraph_font)
        self.browse_numbers_file_button.setText("Browse")
        self.browse_numbers_file_button.clicked.connect(self.browse_numbers_file_button_clicked)
        self.browse_numbers_file_button.setFixedSize(int(self.width() // 5.5), int(self.height() // 12))
        self.browse_numbers_file_button.setStyleSheet("""QPushButton{border: 0px; border-radius: 20px; 
        background-color: #041a3d; color: white;}""")

        self.convert_to_emails_button = QPushButton()
        self.convert_to_emails_button.setFont(self.paragraph_font)
        self.convert_to_emails_button.setText("Convert!")
        self.convert_to_emails_button.clicked.connect(self.convert_to_emails_button_clicked)
        self.convert_to_emails_button.setFixedSize(int(self.width() // 4.2), int(self.height() // 10))
        self.convert_to_emails_button.setStyleSheet("""QPushButton{border: 0px; border-radius: 15px; 
        background-color: green; color: white;}""")

        # adding widgets to child layouts
        self.header_layout.addWidget(self.welcome_label, alignment=Qt.AlignHCenter)
        self.header_layout.addWidget(self.modules_and_libraries_used_label, alignment=Qt.AlignHCenter)

        self.child_numbers_layout.addWidget(self.numbers_label)
        self.child_numbers_layout.addWidget(self.get_numbers_file_location)
        self.child_numbers_layout.addWidget(self.browse_numbers_file_button)

        self.clearout_phone_fields_groupbox.setLayout(self.child_numbers_layout)
        self.footer_layout.addWidget(self.convert_to_emails_button)

        # adding child widgets to parent body layout
        self.body_layout.addWidget(self.clearout_phone_fields_label)
        self.body_layout.addSpacing(10)
        self.body_layout.addWidget(self.clearout_phone_fields_groupbox)
        self.body_layout.addStretch()

        # adding child layouts to master layout
        self.master_layout.addLayout(self.header_layout)
        self.master_layout.addStretch()
        self.master_layout.addLayout(self.body_layout)
        self.master_layout.addStretch()
        self.master_layout.addLayout(self.footer_layout)
        self.master_layout.addStretch()

        self.setLayout(self.master_layout)

    def browse_numbers_file_button_clicked(self):
        number_file_location = QFileDialog.getOpenFileName(self, "Choose numbers file", "", "Text File (*.txt)")
        self.numbers_file_location = number_file_location[0]

        # setting location to self.get_numbers_file_location
        self.get_numbers_file_location.setText(self.numbers_file_location)

    def convert_to_emails_button_clicked(self):
        # reading numbers .txt file
        with open(self.numbers_file_location) as number_file:
            cleaned_numbers_list = eval(number_file.read())

        # triggering validate_numbers_with_api method
        self.validate_numbers_with_api(payload=cleaned_numbers_list)

        # creating dataframe to store email addresses
        self.pandas_dataframe = pd.DataFrame({"Email Addresses": self.cleaned_emails})

        # save file dialog box
        save_excel_file = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel File (*.xlsx)")
        cleaned_save_excel_file_location = save_excel_file[0]

        # saving dataframe into chosen file
        self.pandas_dataframe.to_excel(cleaned_save_excel_file_location, index=False)

        # clearing self.get_numbers_file_location
        self.get_numbers_file_location.clear()

    def validate_numbers_with_api(self, payload):
        # default api header
        api_headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer: 8c1963a796303e23a4c6bb15fdb399f2"
                             ":0239195f772cda665994bdc8895e80ca4937fd644ceb93b8305e58d04d81a128 "
        }

        self.cleaned_emails = []
        for number in payload:
            cleaned_number = '"' + number + '"'
            api_data = '{ "number": ' + cleaned_number + ', "country_code": "US" }'

            clearout_api_response = requests.post(self.clearout_phone_api, data=api_data, headers=api_headers).json()
            response_valid = clearout_api_response['data']['status']
            response_carrier = clearout_api_response['data']['carrier']
            response_mobility = clearout_api_response['data']['line_type']

            if response_valid == "valid" and response_mobility == "mobile":
                carrier_convert = self.determine_carrier_name(carrier_name=response_carrier)
                email_format = number + carrier_convert
                self.cleaned_emails.append(email_format)

            else:
                print('error: landline or invalid number ', number)

            time.sleep(3)

    @staticmethod
    def determine_carrier_name(carrier_name):
        verizon = 'Verizon Wireless'
        verizon2 = 'CELLCO PARTNERSHIP DBA VERIZON'
        verizon_email = '@vtext.com'
        att = 'AT&T Wireless'
        att_email = '@txt.att.net'
        omni = 'OMNIPOINT COMMUNICATIONS, INC.'
        omni2 = 'OMNIPOINT MIAMI E LICENSE, LLC'
        omni_email = '@omnipoint.com'
        tmobile = 'T-Mobile USA, Inc.'
        tmobile3 = 'T-MOBILE USA, INC.'
        tmo4 = 'SUNCOM DBA T-MOBILE USA'
        tmo4sun = '@tms.suncom.com'
        tmobile_email = '@tmomail.net'
        tmo = 'T-Mobile'
        tmo_email = '@tmomail.net'
        pwtel = 'POWERTEL ATLANTA LICENSES, INC'
        pwtel_email = '@ptel.net'
        aerial = 'AERIAL COMMUNICATIONS'
        metropcs = 'METRO PCS, INC.'
        metro_email = '@mymetropcs.com'
        sprint = 'Sprint Wireless'
        sprint2 = 'SPRINT SPECTRUM L.P.'
        sprint_email = '@messaging.sprintpcs.com'
        cricket = 'Cricket Wireless - ATT - SVR'
        cricket_email = '@sms.cricketwireless.net'
        error_message = 'error: Bad carrier name, go find my name' + carrier_name
        if carrier_name == verizon or carrier_name == verizon2:
            return verizon_email
        elif carrier_name == att:
            return att_email
        elif carrier_name == tmobile or carrier_name == tmobile3:
            return tmobile_email
        elif carrier_name == tmo4:
            return tmo4sun
        elif carrier_name == tmo or carrier_name == aerial:
            return tmo_email
        elif carrier_name == omni or carrier_name == omni2:
            return omni_email
        elif carrier_name == metropcs:
            return metro_email
        elif carrier_name == pwtel:
            return pwtel_email
        elif carrier_name == sprint or carrier_name == sprint2:
            return sprint_email
        elif carrier_name == cricket:
            return cricket_email
        else:
            return error_message
