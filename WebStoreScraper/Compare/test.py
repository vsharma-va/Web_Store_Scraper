import WebStoreScraper.Reliance_Digital.Reliance_Digital as Reliance
import WebStoreScraper.Amazon.Amazon as Amazon
import WebStoreScraper.Flipkart.Flipkart as Flipkart

# change the path of geckodriver to Resources/geckodriver.exe when creating the exe
if __name__ == '__main__':
    user_input = input('''Do you want to search amazon
Type yes to include
Type no to skip:  ''')
    if user_input.lower() == 'yes':
        Amazon.main()
    elif user_input.lower() == 'no':
        print('Amazon Skipped')
    user_input = input('''Do you want to search Flipkart
Type yes to include
Type no to skip:  ''')
    if user_input.lower() == 'yes':
        Flipkart.main()
    elif user_input.lower() == 'no':
        print('Flipkart Skipped')
    user_input = input('''Do you want to search Reliance Digital
Type yes to include
Type no to skip:  ''')
    if user_input.lower() == 'yes':
        Reliance.main()
    elif user_input.lower() == 'no':
        print('Reliance Digital Skipped')

    print("Completed")
