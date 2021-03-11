import pandas as pd

def parse(files):
    df = pd.DataFrame()
    for f in files:
        df_t = pd.read_csv(f, sep='\n', names=['Speech'])
        df_t['Speaker'] = f.strip('.txt')
        df = pd.concat([df, df_t])
    df.reset_index(drop=True, inplace=True)
    return df


def extra_plots():
    df = pd.DataFrame(columns=['plot', 'movie_name'])
    df = df.append({"plot":"Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle station, while also attempting to rescue Princess Leia from the mysterious Darth Vader.", "movie_name" :"Star Wars"}, ignore_index=True)
    df = df.append({"plot":"Austin Powers is a 60's spy who is cryonically frozen and released in the 1990's. The world is a very different place for Powers. Unfortunately for Austin, everyone is no longer sex-mad. Although he may be in a different decade, his mission is still the same. He has teamed up with Vanessa Kensington to stop the evil Dr. Evil, who was also frozen in the past. Dr. Evil stole a nuclear weapon and is demanding a payment of (when he realises its the 90's) 100 billion dollars. Can Austin Powers stop this madman? or will he caught up with Evil's henchman, with names like Alotta Fagina and Random Task? Only time will tell!", "movie_name" :"Austin Powers"}, ignore_index=True)
    df = df.append({"plot":"The Dark Knight of Gotham City confronts a dastardly duo: Two-Face and the Riddler. Formerly District Attorney Harvey Dent, Two-Face incorrectly believes Batman caused the courtroom accident which left him disfigured on one side; he has unleashed a reign of terror on the good people of Gotham. Edward Nygma, computer-genius and former employee of millionaire Bruce Wayne, is out to get the philanthropist; as The Riddler he perfects a device for draining information from all the brains in Gotham, including Bruce Wayne's knowledge of his other identity. Batman/Wayne is/are the love focus of Dr. Chase Meridan. Former circus acrobat Dick Grayson, his family killed by Two-Face, becomes Wayne's ward and Batman's new partner Robin the Boy Wonder.", "movie_name" :"Batman Forever"}, ignore_index=True)
    df = df.append({"plot":"Huge advancements in scientific technology have enabled a mogul to create an island full of living dinosaurs. John Hammond has invited four individuals, along with his two grandchildren, to join him at Jurassic Park. But will everything go according to plan? A park employee attempts to steal dinosaur embryos, critical security systems are shut down and it now becomes a race for survival with dinosaurs roaming freely over the island.", "movie_name" :"Jurassic Park"}, ignore_index=True)
    df = df.append({"plot":"F.B.I. trainee Clarice Starling (Jodie Foster) works hard to advance her career, while trying to hide or put behind her West Virginia roots, of which if some knew, would automatically classify her as being backward or white trash. After graduation, she aspires to work in the agency's Behavioral Science Unit under the leadership of Jack Crawford (Scott Glenn). While she is still a trainee, Crawford asks her to question Dr. Hannibal Lecter (Sir Anthony Hopkins), a psychiatrist imprisoned, thus far, for eight years in maximum security isolation for being a serial killer who cannibalized his victims. Clarice is able to figure out the assignment is to pick Lecter's brains to help them solve another serial murder case, that of someone coined by the media as 'Buffalo Bill' (Ted Levine), who has so far killed five victims, all located in the eastern U.S., all young women, who are slightly overweight (especially around the hips), all who were drowned in natural bodies of water, and all who were stripped of large swaths of skin. She also figures that Crawford chose her, as a woman, to be able to trigger some emotional response from Lecter. After speaking to Lecter for the first time, she realizes that everything with him will be a psychological game, with her often having to read between the very cryptic lines he provides. She has to decide how much she will play along, as his request in return for talking to him is to expose herself emotionally to him. The case takes a more dire turn when a sixth victim is discovered, this one from who they are able to retrieve a key piece of evidence, if Lecter is being forthright as to its meaning. A potential seventh victim is high profile Catherine Martin (Brooke Smith), the daughter of Senator Ruth Martin (Diane Baker), which places greater scrutiny on the case as they search for a hopefully still alive Catherine. Who may factor into what happens is Dr. Frederick Chilton (Anthony Heald), the warden at the prison, an opportunist who sees the higher profile with Catherine, meaning a higher profile for himself if he can insert himself successfully into the proceedings.", "movie_name" :"The silence of the lambs"}, ignore_index=True)
    df = df.append({"plot":"Thomas A. Anderson is a man living two lives. By day he is an average computer programmer and by night a hacker known as Neo. Neo has always questioned his reality, but the truth is far beyond his imagination. Neo finds himself targeted by the police when he is contacted by Morpheus, a legendary computer hacker branded a terrorist by the government. As a rebel against the machines, Neo must confront the agents: super-powerful computer programs devoted to stopping Neo and the entire human rebellion.", "movie_name" :"The Matrix"}, ignore_index=True)
    df = df.append({"plot":"Based off of the comic book. Unbeknownst to other people, there is a private agency code named MiB. This agency is some kind of extra terrestrial surveillance corporation. Then, one of the agency's finest men only going by the name 'K' (Tommy Lee Jones) ,is recruiting for a new addition to the agency. He has chosen James Edwards (Will Smith) of the N.Y.P.D. Then, one day, a flying saucer crashes into Earth. This was an alien a part of the 'Bug' race. He takes the body of a farmer (Vincent D'Onofrio) and heads to New York. He is searching for a super energy source called 'The Galaxy'. Now, Agents J and K must stop the bug before it can escape with the galaxy." , "movie_name" :"Men in Black"}, ignore_index=True)
    df = df.append({"plot":"Jack Skellington, the pumpkin king of Halloween Town, is bored with doing the same thing every year for Halloween. One day he stumbles into Christmas Town, and is so taken with the idea of Christmas that he tries to get the resident bats, ghouls, and goblins of Halloween Town to help him put on Christmas instead of Halloween -- but alas, they can't get it quite right.", "movie_name" :"The Nightmare before Christmas"}, ignore_index=True)
    df = df.append({"plot":"This swash-buckling tale follows the quest of Captain Jack Sparrow, a savvy pirate, and Will Turner, a resourceful blacksmith, as they search for Elizabeth Swann. Elizabeth, the daughter of the governor and the love of Will's life, has been kidnapped by the feared Captain Barbossa. Little do they know, but the fierce and clever Barbossa has been cursed. He, along with his large crew, are under an ancient curse, doomed for eternity to neither live, nor die. That is, unless a blood sacrifice is made.", "movie_name" :"Pirates of the Caribbean"}, ignore_index=True)
    df = df.append({"plot":"Since birth, a big fat lie defines the well-organised but humdrum life of the kind-hearted insurance salesman and ambitious explorer, Truman Burbank. Utterly unaware of the thousands of cleverly hidden cameras watching his every move, for nearly three decades, Truman's entire existence pivots around the will and the wild imagination of the ruthlessly manipulative television producer, Christof--the all-powerful TV-God of an extreme 24/7 reality show: The Truman Show. As a result, Truman's picturesque neighbourhood with the manicured lawns and the uncannily perfect residents is nothing but an elaborate state-of-the-art set, and the only truth he knows is what the worldwide television network and its deep financial interests dictate. Do lab rats know they are forever imprisoned?", "movie_name" :"The Truman Show"}, ignore_index=True)
    return df