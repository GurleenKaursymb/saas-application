//This will basically serve as the initialisation point for every single page in our application. 

import type { AppProps } from 'next/app'; 
//So this line of code tells the computer to  geab a set of rules called AppProps from the web building framewrok Next.js

import '../styles/globals.css';  // This imports Tailwind styles

export default function MyApp({ Component, pageProps }: AppProps) {
  /*
This creates the main fucntion named myApp and makes it available for the rest of your code to use.
{ Component, pageProps } : these are the two things my function will take in - Component is whatever specific page a 
 user is trying to visit right now. 
 pageProps is the specific data or information that page needs to load.
 : AppProps to ensure that it fllows our imported rules/ 
*/
  return <Component {...pageProps} />;
  //So basially the function takes the page thay the user wants to see and gives it its data (pageProps) and throws it onto the screen 
}