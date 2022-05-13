import React, { Component, useState } from 'react';
import { Button, Divider, Form, Grid, Header, Segment, Message, Image } from 'semantic-ui-react';
import axios from "axios";
import { useNavigate } from "react-router-dom";

const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/users/'
})


function RegisterPage() {

    localStorage.removeItem("userID");
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    /* Error is integer
     * 0 = no error, 1 = username taken
     * 2 = email taken, 3 = email invalid
     * 4 = password mismatch, 5 = form incomplete
     */
    const [error, setError] = useState(false);

    function login() {
        navigate('/login');
    }

    function checkSignup() {
        if (username === '' || email === '' || password === '' || confirmPassword === '') {
            setError(5);
        } else if (password != confirmPassword) {
            setError(4);
        }
        else {
            api.post('/new', {
                "u_email": email,
                "u_password": password,
                "username": username,
                "isAdmin": false
            }).then(res => {
                localStorage.setItem("userID", res.data["User ID"]);
                localStorage.setItem("username", res.data["Username"]);
                localStorage.setItem("isAdmin", res.data["IsAdmin"]);
                login();
            }).catch(error => {
                console.log(error.response.data);
                if (error.response.data == "Enter Valid Email") {
                    setError(3)
                } if (error.response.data == "Username already taken") {
                    setError(1)
                } if (error.response.data == "Email already taken") {
                    setError(2)
                }
                if (error.response.status == 404) {
                    console.log("User or password incorrect");
                }
            })
        }
    }

    return <>
        <Segment inverted>
            <Header
                as='h1'
                textAlign='center'
                style={{
                    fontSize: '5em',
                    fontWeight: 'bold',
                    color: '#2ed24b'
                }}> <Image rounded style={{ width: '85px' }} src='/rumzon-logo.jpeg' /> UMZON </Header>
            <Segment placeholder invert>
                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <Header
                            as='h2'
                            content='RUMZON'
                            textAlign='center'
                            style={{
                                fontSize: '2.5em',
                                fontWeight: 'bold',
                                paddingBottom: '1em'
                            }}> Create a New Account </Header>
                        <Form>
                            <Form.Input
                                icon='user'
                                iconPosition='left'
                                label='Username'
                                placeholder='Username'
                                error={(error === 5 && username === '')}
                                value={username}
                                onChange={input => setUsername(input.target.value)}
                            />
                            <Form.Input
                                icon='mail'
                                iconPosition='left'
                                label='Email'
                                placeholder='Email'
                                error={(error === 5 && email === '')}
                                value={email}
                                onChange={input => setEmail(input.target.value)}
                            />
                            <Form.Input
                                icon='lock'
                                iconPosition='left'
                                placeholder='Password'
                                label='Password'
                                type='password'
                                error={(error === 5 && password === '')}
                                value={password}
                                onChange={input => setPassword(input.target.value)}
                            />
                            <Form.Input
                                icon='lock'
                                iconPosition='left'
                                placeholder='Confirm Password'
                                label='Confirm Password'
                                type='password'
                                error={(error === 5 && confirmPassword === '')}
                                value={confirmPassword}
                                onChange={input => setConfirmPassword(input.target.value)}
                            />
                            <Message
                                hidden={error != 1}
                                color={'red'}
                                header='Username already taken.'
                            />
                            <Message
                                hidden={error != 2}
                                color={'red'}
                                header='Email already taken.'
                            />
                            <Message
                                hidden={error != 3}
                                color={'red'}
                                header='Please enter a valid email.'
                            />
                            <Message
                                hidden={error != 4}
                                color={'red'}
                                header='Passwords do not match.'
                            />
                            <Message
                                hidden={error != 5}
                                color={'red'}
                                header='Please fill out the form.'
                            />
                            <Button content='Sign Up' icon='signup' primary onClick={checkSignup} />
                        </Form>
                    </Grid.Column>
                    <Grid.Column verticalAlign='middle'>
                        <Header
                            as='h2'
                            content='RUMZON'
                            textAlign='center'
                            style={{
                                fontWeight: 'bold',
                            }}> Already have an account? </Header>
                        <Button content='Log in' size='small' primary onClick={login} />
                    </Grid.Column>
                </Grid>

                <Divider vertical>Or</Divider>
            </Segment>
        </Segment>
    </>
}

export default RegisterPage;
