import React, { Component } from 'react'
import Typography from '@material-ui/core/Typography'
import { TextField } from '@material-ui/core'
import Button from '@material-ui/core/Button'
import Grid from '@material-ui/core/Grid'
import withStyles from '@material-ui/styles/withStyles'
import { withRouter } from 'react-router-dom'
import Util from '../Util'
import Link from 'react-router-dom/Link'

const styles = theme => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.grey['100'],
    overflow: 'hidden',
    backgroundSize: 'cover',
    backgroundPosition: '0 400px',
    paddingBottom: 200,
    alignContent: 'center',
    alignItems: 'center',
    width: 1000
  },
  grid: {
    width: 1200,
    marginTop: 40,
    [theme.breakpoints.down('sm')]: {
      width: 'calc(100% - 20px)'
    },
  },
  panel: {
    width: 1000,
    marginTop: 40,
    [theme.breakpoints.down('sm')]: {
      width: 'calc(100% - 20px)'
    },
  },
  paper: {
    padding: theme.spacing(3),
    textAlign: 'left',
    color: theme.palette.text.secondary,
  },
  rangeLabel: {
    display: 'flex',
    justifyContent: 'space-between',
    paddingTop: theme.spacing(2)
  },
  topBar: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 32
  },
  outlinedButtom: {
    textTransform: 'uppercase',
    margin: theme.spacing(1)
  },
  actionButtom: {
    textTransform: 'uppercase',
    margin: theme.spacing(1),
    width: 152
  },
  blockCenter: {
    padding: theme.spacing(2),
    textAlign: 'center'
  },
  block: {
    padding: theme.spacing(2),
  },
  box: {
    marginBottom: 40,
    height: 120
  },
  tallBox: {
    marginBottom: 40,
    height: 320
  },
  inlining: {
    display: 'inline-block',
    marginRight: 10
  },
  buttonBar: {
    display: 'flex'
  },
  alignRight: {
    display: 'flex',
    justifyContent: 'flex-end'
  },
  noBorder: {
    borderBottomStyle: 'hidden'
  },
  loadingState: {
    opacity: 0.05
  },
  loadingMessage: {
    position: 'absolute',
    top: '40%',
    left: '40%'
  },
  gridListWrapper: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.paper,
  },
  fontResize: {
    fontSize: 20
  }
})

// function goToNextFunc(cl) {
//   cl.setState({ done: false })
//   cl.setState({ answered: false })
//   cl.setState({ showAnswer: false })

//   // Need to hide answer for page loading
//   cl.setState({ notMovingOn: true })
//   this.props.cancelFcn()
// }

// // After guessing screen reloads, reset page
// function cleanup(cl) {
//   // cl.setState({ notMovingOn: true })
// }

class Quiz extends Component {
  constructor(props) {
    super(props)
    this.state = {
      question: 0,  // which question
      answered: false, // whether question answered or not
      text: "", // submitted user text
      done: false,  // finished all questions for this func, so don't show next Q button
      showAnswer: false, // show answer for function or not
      notMovingOn: true, // stop showing answer in case next page loads before we navigate to guessing screen
      gotItRight: false,
    }
  }

  funcObj = this.props.funcObj
  inputGens = this.props.funcObj.inputGenerators()
  currInput = ""
  answerText = ""

  questionInput = () => {
    var newInput = this.inputGens[this.state.question]()
    this.currInput = newInput
    return newInput
  }

  submitAnswer = (submitted) => {
    if (submitted === "") {
      alert("Please submit an answer!")
      return
    }
    if (!this.funcObj.validOutput(submitted)) {
      alert("'" + submitted + "' is not a valid output of this function")
      return
    }

    const actual = this.funcObj.function(this.currInput)
    const submittedAsVal = this.funcObj.parseOutput(submitted)
    // console.log(actual)
    // console.log(submittedAsVal)
    const gotCorrect = this.funcObj.equivalentOutputs(submittedAsVal, actual)

    //Construct action object and send to server 
    if (localStorage.getItem(this.funcObj.description()) === null) {
      var action = {}
      action.id = localStorage.getItem('userID')
      action.fcn = this.funcObj.description()
      action.type = "quiz_answer"
      action.in = this.funcObj.inputDBStr(this.currInput)
      action.out = this.funcObj.outputDBStr(submittedAsVal)
      action.q = this.state.question.toString()
      action.actual = this.funcObj.outputDBStr(actual)
      action.result = gotCorrect.toString()
      action.time = Util.getCurrentTime()
      // console.log(action)
      action.key = Util.newKey()
      Util.sendToServer(action)

      console.log("'", action.in, "'")
      console.log("'", action.out, "'")
      console.log("'", action.actual, "'")
    }

    // Show answer onscreen
    var answerText = ""
    if (gotCorrect) {
      answerText = "Nice, that's correct!"
    } else {
      answerText = "Incorrect."
    }
    this.setState({ 'answerText': answerText })

    if (this.state.question + 1 < this.inputGens.length) {
      this.setState({ 'answered': true })
    } else {
      this.setState({ done: true })
    }

    if (gotCorrect) {
      this.setState({ gotItRight: true })
    } else {
      this.setState({ gotItRight: false })
    }
  }

  goToNextQuestion = () => {
    if (this.state.question + 1 < this.inputGens.length) {
      this.setState({
        question: this.state.question + 1,
        answered: false,
        text: "",
        answerText: ""
      })
    }
  }

  submitFinalGuess = () => {
    // Construct and submit final answer to server
    var guess = Object()
    guess.id = localStorage.getItem('userID')
    guess.fcn = this.funcObj.description()
    guess.type = "final_answer"
    guess.finalGuess = this.props.guessText
    guess.time = Util.getCurrentTime()

    if (localStorage.getItem(this.funcObj.description()) === null) {
      guess.key = Util.newKey()
      localStorage.setItem(this.funcObj.description(), 'Done')
      Util.sendToServer(guess)
    }
    this.setState({
      showAnswer: true
    })
  }

  toNextFuncButton = (nextPage) => {
    if (nextPage === undefined) {
      return (<div></div>)
    }
    return (
      <div>
        <Button variant="contained" className={this.props.actionButton} onClick={this.props.cancelFcn}>
          <Link style={{ color: '#FFF' }} to={nextPage}> go to next mystery function</Link>
        </Button>
      </div>
    )
  }

  answerComponent = () => {
    return (
      <div>
        <Grid item>
          <Typography variant="h5">Your answer</Typography>
          <Typography variant="h6">{this.props.guessText}</Typography>
          <Typography variant="h1">

            - - - - - - - -

          </Typography>
          <Typography variant="h5">Our answer</Typography>
          <Typography variant="h6">{this.props.funcObj.answerText()}</Typography>
        </Grid>
        <Grid item>
          {this.toNextFuncButton(this.props.nextPage)}
        </Grid>
      </div>
    )
  }

  submitGuessButton = () => {
    return (
      <Grid item>
        <Button color='primary' variant="contained" type="submit" onClick={this.submitFinalGuess}>
          <Typography variant="h4">Submit guess and see answer</Typography>
        </Button>
      </Grid>
    )
  }

  nextQuestionButton = () => {
    return (
      < Grid item >
        <Button variant="contained" type="submit" onClick={this.goToNextQuestion}>
          Next Question
        </Button>
      </Grid >
    )
  }

  giveUpButton = () => {
    return (
      <Grid item>
        <Button variant="contained" type="submit" onClick={this.submitFinalGuess}>
          Give up and show answer
        </Button>
      </Grid>
    )
  }

  questionDisplay = (my_classes) => {
    return (
      <div>
        <Grid item>
          <Typography variant="h4">Question {this.state.question + 1} out of {this.inputGens.length}:  </Typography>
          <Typography variant="h3">What would this function output for {this.funcObj.inputDisplayStr(this.questionInput())}? </Typography>

          <TextField InputProps={{ classes: { input: my_classes.fontResize } }} onChange={(e) => { this.setState({ text: e.target.value }) }} value={this.state.text} onKeyUp={(e) => { if (e.keyCode === 13) { this.submitAnswer(e.target.value) } }} helperText="ENTER to submit">
          </TextField>
        </Grid>
        <Grid padding={8} margin={8} item>
          <Typography variant="h5">{this.state.answerText}</Typography>
        </Grid>
      </div>
    )
  }

  retractGuessButton = () => {
    return (
      <div>
        <Grid item>
          <Button variant="contained" type="submit" onClick={this.props.cancelFcn}>
            Retract guess and go back to evaluator
          </Button>
        </Grid>
      </div>
    )
  }


  render() {
    var my_classes = this.props;
    return (
      <div>
        < Grid container item spacing={6} className={my_classes.panel}>
          < Grid item>
            {
              this.state.showAnswer ?
                null
                :
                <div>{
                  this.state.answered ?
                    <div>{
                      this.state.gotItRight ?
                        null
                        :
                        <div>{this.retractGuessButton()}</div>
                    }</div>
                    : null
                }
                </div>
            }
          </ Grid>
          <Grid item>
            {
              this.state.showAnswer ?
                <div>{this.answerComponent()}</div>
                :
                <div>
                  {
                    this.state.notMovingOn ?
                      <div>{this.questionDisplay(my_classes)}</div>
                      :
                      null}
                </div>
            }
          </Grid>
          < Grid item>
            {this.state.done ?
              null
              :
              <div>
                {
                  this.state.showAnswer ?
                    null
                    :
                    <div>{
                      this.state.answered ?
                        <div>{
                          this.state.gotItRight ?
                            <div>{this.nextQuestionButton()}</div>
                            :
                            <div>{this.giveUpButton()}</div>
                        }</div>
                        : null
                    }
                    </div>
                }</div>
            }
          </ Grid>
          < Grid item>
            {
              this.state.showAnswer ?
                null
                :
                <div>{
                  this.state.done ?
                    <div>{this.submitGuessButton()}</div>
                    :
                    null
                }</div>
            }
          </Grid>
        </Grid>
      </div>
    )
  }
}

export default withRouter(withStyles(styles)(Quiz));