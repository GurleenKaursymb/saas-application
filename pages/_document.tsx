import { Html, Head, Main, NextScript } from 'next/document';
//bsically first we are imporring four essential things from Next.js - html, head, main, nextscript
export default function Document() { //to ccreate a main blueprint funciton called document and making it available for our project to use automatically. 

  return (
    <Html lang="en">
      {/*This is to explicitly tthe web browsers and search engines that everything isnside here is a webpage
      and the primary language used on this site is englsih */}
      <Head>
        <title>Business Idea Generator</title>
        {/*this is the text which appears on the browser tab at the very top of your screen  */}
        <meta name="description" content="AI-powered business idea generation" />
      </Head>
      <body>
        <Main />
        <NextScript /> {/*loads the hidden scripts that make the website fast, interactive, 
        and smooth when people click around. */}
      </body>
    </Html>
  );
}