import React from 'react'
import { Route, HashRouter, Switch } from 'react-router-dom'
import GuessingScreen from './screens/GuessingScreen'
import StartScreen from './screens/StartScreen'
import IsPalindromeListInts from './functions/IsPalindromeListInts';
import ThankYouScreen from './screens/ThankYouScreen';
import IsPalindromeString from './functions/IsPalindromeString';
import MakePalindrome from './functions/MakePalindrome';


// Logic to randomize screen order would go here
// -> have a start page that is just a button
// have an array of random paths and also funcObjs
// shuffle the funcObjs, and then assign at random with the links 

export default props => (
  <HashRouter>
    <Switch>
      <Route exact path='/' render={(props) => <StartScreen {...props} nextPage='/first'></StartScreen>} />
      <Route exact path='/first' render={(props) => <GuessingScreen {...props} funcObj={IsPalindromeString} nextPage={'/last'}></GuessingScreen>} />
      <Route exact path='/last' render={(props) => <ThankYouScreen></ThankYouScreen>} />
    </Switch>
  </HashRouter>
)