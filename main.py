import os
import argparse
from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser(add_help=True, allow_abbrev=False)
    # Acepts two commands: extract_predictions and find_winners
    sub_parsers = parser.add_subparsers(dest='command', help='The command to run.')
    extract_parser = sub_parsers.add_parser('extract_predictions', help='Extracts the predictions from the html file.')
    find_winners_parser = sub_parsers.add_parser('find_winners', help='Finds the winners of the predictions.')
    
    # Arguments for the extract_predictions command
    extract_parser.add_argument('--html', required=False ,default="score.html", help='The html file to extract the predictions from.')

    # Arguments for the find_winners command
    find_winners_parser.add_argument('--score', help='The score of the game.')
    find_winners_parser.add_argument('--html', required=False, default="score.html", help='The html file to extract the predictions from.')

    args = parser.parse_args()




    def extract(html):
        """ Loads the html file score.html and extracts the text from it."""
        with open(html, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            body = soup.find('body')
            modal = body.find('div', {'class': 'modal'})
            modal_body = modal.find('div', {'class': 'modal-body'})
            table = modal_body.find('table')
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            # Remove the file if it already exists
            if os.path.exists('score.csv'):
                os.remove('score.csv')
            data = []
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols][:2]
                data.append([ele for ele in cols if ele])
                # Write the data to a csv file
                with open('score.csv', 'a') as f:
                    f.write(','.join(cols) + '\n')
            return data
        
    def find_winners(score, html='score.html'):
        """ Applies the rules to the extracted data and returns the winners."""
        data = extract('score.html')
        score = score.replace(' ', '')
        winners = []
        home_score = int(score.split('-')[0])
        away_score = int(score.split('-')[1])
        # Rule 1: If the score is perfect match then the winner is the person who predicted it.
        for i in data:
            if i[1].replace(' ', '') == score:
                winners.append(i[0])

        # Rule 2: If the score is not a perfect match then the winner is the person who predicted the goal difference correctly.
        # Example: If the score is 2-1 and the predicted scores are 1-0, 3-2, 4-1 then the winner is the persons who predicted 3-2 and 1-0.
        if not winners:
            print("Rule 2 Applied")
            for i in data:
                if int(i[1].split('-')[0]) - int(i[1].split('-')[1]) == home_score - away_score:
                    winners.append(i[0])
        
        # Rule 3: If no one predicted the goal difference then the winner is the persons who predicted the correct winner.
        if not winners:
            print("Rule 3 Applied")
            for i in data:
                if (home_score > away_score and int(i[1].split('-')[0]) > int(i[1].split('-')[1])) or (home_score < away_score and int(i[1].split('-')[0]) < int(i[1].split('-')[1])):
                    winners.append(i[0])

        print("\n".join(winners))

        return winners

    if args.command == 'extract_predictions':
        extract(args.html)

    if args.command == 'find_winners':
        find_winners(args.score, args.html)

if __name__ == '__main__':
    main()