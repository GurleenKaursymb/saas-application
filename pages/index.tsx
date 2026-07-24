/*
This is a Next.js react component - using tailwind CSS for styling which acts as the frontend for a simple 
web application. 
purpose: Fetch a random business idea from a backend API and display it on the screen  
*/

"use client" 
//Tells next.js that this is a Client Component - explicitly tells Next.js to run this on the user's browser. 

import { useEffect, useState } from 'react';

/*
This imports two important React built-in helper functions (hooks). 

Usestate: used to store and update data like the business idea insid the Component

useEffect: used to trigger side effects, in this case - feteching data from API as soon as the page finishes 
loading
*/

export default function Home() {
  //This defines thw main react component called Home and xports it to Next.js knows to render it as the main page

    const [idea, setIdea] = useState<string>('…loading');
    /*
    This is bassically setting uy=p a dynamic display board. idea is the actual text which will show up on the screen. 
    Right now it is set to display '....loading' by default. 

    SetIdea is a special tool used to change what the display says. Its like a remote which will be used to chanyge 
    the text from ...loading to the actual idea. 

    <string> is the rule telling the computer that this display board is only alllowed to show text letters adnd
    not numbers or images. 
     */

    useEffect(() => { //starts the hook which will run the code aftet the component first appears on the screen. 
        fetch('/api/') 
        /* This is an HTTP request to /api which is a backend endpoint on the same server - to ask for the 
        business idea */
            .then(res => res.text()) 
            //Once the server responds this line is to convert that raw response into plain text. 
            .then(setIdea)//The plain text/ business idea is passed into the setIdea function 
            //so idea is updated from loading to the actual business text
            .catch(err => setIdea('Error: ' + err.message));
            //If somehting goes wrong idea will be updated to display the error message instead of the application crashing

    }, []);
// [] this empty arrray is important because now React knows that this whiole fetch code needs to be run only 
//once when the page first loads - so the inifnite loop of fetching and relaodng is avoided. 

// Now to render the UI: 
    return (
        <main className="p-8 font-sans">
          {/*p-8: adds space of about 32 px around the whole page and font-sans is to fix the font to sans-serif */}
            <h1 className="text-3xl font-bold mb-4">
                Business Idea Generator
            </h1>
            {/*This is for the main title of the page:
            text-3xl makes the text quite large 
            font bold makes the title bold. 
            mb-4 adds a margin at the bottom to push the coontent below it down. 
            */}
            <div className="w-full max-w-2xl p-6 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm">
{/*This is to create a stylised container card to hold the business idea.
w-full max-w-2xl : this makes the card responsive - full width for small screens and capped at a nice size on larger screens 
bg-white dark:bg-gray-800: this sets a white background, but automatically switches to dark gray if user is in dark mode 
border border-gray-300 rounded-lg: Gives the card rounded corners and a light border. 
*/}
                <p className="text-gray-900 dark:text-gray-100 whitespace-pre-wrap">
                    {idea}
                </p>
                {/* Prints the idea text onto thr screen. 
                whitespace-pre-wrap: A very useful CSS class that preserves line breaks and spacing. If the 
                generated business idea is a multi-paragraph plan, it won't bunch up into a single ugly block of text. */}
            </div>
        </main>
    );
}