import React, { Component, useState } from 'react';
import { Button, Divider, Form, Grid, Header, Segment, Message, Image } from 'semantic-ui-react';
import axios from "axios";
import { useNavigate } from "react-router-dom";

const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/users/'
})


function LoginPage(){

    localStorage.removeItem("userID");
    const navigate = useNavigate();
    const [user, setUser] = useState('');
    const [password, setPassword] = useState('');
    const [wrongLogin, setWrongLogin] = useState(false);
    const [enterCredentials, setEnterCredentials] = useState(false);
    //handleChange = (e, { name, value }) => this.setState({ [name]: value })

    function login() {
        navigate('/');
    }
    
    function register() {
        navigate('/register');
    }

    function checkLogin(){
        api.post('/login', { "user": user, "password": password }).then(res => {
            setEnterCredentials(false);
            setWrongLogin(false);
            localStorage.setItem("userID", res.data["User ID"]);
            localStorage.setItem("username", res.data["Username"]);
            localStorage.setItem("isAdmin", res.data["IsAdmin"]);
            login();
        }).catch(error => {
            if (error.response.status == 400) {
                console.log("Incomplete form probably");
                setWrongLogin(false);
                setEnterCredentials(true);
            }
            if (error.response.status == 404) {
                console.log("User or password incorrect");
                setEnterCredentials(false);
                setWrongLogin(true);
            }
        })
    }
            
    return<> 
        <Segment inverted>
            <Header
                as='h1'
                textAlign='center'
                style={{
                    fontSize: '5em',
                    fontWeight: 'bold',
                    color:'#2ed24b'
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
                            }}> Log In </Header>
                        <Form>
                            <Form.Input
                                icon='user'
                                iconPosition='left'
                                label='Username or Email'
                                placeholder='Username or Email'
                                value={user}
                                onChange={input => setUser(input.target.value)}
                            />
                            <Form.Input
                                icon='lock'
                                iconPosition='left'    
                                label='Password'
                                type='password'
                                placeholder='Password'
                                value={password}
                                onChange={input => setPassword(input.target.value)}
                            />
                            <Message
                                hidden={!wrongLogin}
                                color={'red'}
                                header='User or password incorrect.'
                            />
                            <Message
                                hidden={!enterCredentials}
                                color={'red'}
                                header='Please enter your username/email and password.'
                            />
                            <Button content='Log in' primary onClick={checkLogin} />
                        </Form>
                    </Grid.Column>
                    <Grid.Column verticalAlign='middle'>
                        <Header
                            as='h2'
                            content='RUMZON'
                            textAlign='center'
                            style={{
                                fontWeight: 'bold',
                            }}> Create a new account! </Header>
                        <Button content='Sign up' icon='signup' size='small' primary onClick={() => register()} />
                    </Grid.Column>
                </Grid>

                <Divider vertical>Or</Divider>
            </Segment>
        </Segment>
    </>
}

export default LoginPage;
