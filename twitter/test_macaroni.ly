\version "2.18.2"
\include "english.ly"

\header{
    title = "macarooney tweetest testweet"
}

\score {
    \new Staff {
        \key e \major
        \numericTimeSignature
        \time 5/8
        <cs'' e'' b''>8. <b' e'' a''>16 <as'' e'' a''>16 <a'' e'' gs''>8 <b' e'' a''>8.
    }
}

\paper{
    indent=0\mm
    line-width=120\mm
    oddFooterMarkup=##f
    oddHeaderMarkup=##f
    bookTitleMarkup = ##f
    scoreTitleMarkup = ##f
    }