import React, { Component } from 'react';
import { Message, Modal, Header, Divider, Button, Form } from "semantic-ui-react";
import axios from "axios";


const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/'
})


class Profile extends Component {

    state = {
        items: [],
        loggedIn: false,
        username: '',
        email: '',
        modalMode: '',
        newUser: '',
        newEmail: '',
        newPassword: '',
        confirmPassword: '',
        deleteForm: '',
        enterUsername: false,
        usernameTaken: false,
        enterEmail: false,
        emailTaken: false,
        invalidEmail: false,
        enterPassword: false,
        passwordMismatch: false,
        deleteUser: false,
        deleteFormWrong: false
    }

    constructor() {
        super();
        if (localStorage.getItem("userID") != null) {
            this.getUser();
            this.state.loggedIn = true;
        }
    }

    getUser = () => {
        api.post('/users', {
            "u_id": parseInt(localStorage.getItem("userID"))
        }).then(res => {
            console.log("User:");
            console.log(res.data);
            this.setState({
                username: res.data["Username"],
                email: res.data["Email"]
            });
        }).catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
        })
    }

    deleteUser = () => {
        if (this.state.deleteForm != 'delete') {
            this.setState({ deleteFormWrong: true })
        } else {
            api.delete('/users', {
                data: {
                    "u_id": parseInt(localStorage.getItem("userID"))
                }
            }).then(res => {
                localStorage.removeItem("userID");
                localStorage.removeItem("username");
                localStorage.removeItem("isAdmin");
                window.location.reload(false);
            }).catch(error => {
                console.log(error.response.data);
                console.log(error.response.status);
            })
        }
    }

    render() {
        if (this.state.loggedIn) {
            return <>
                <Header as='h1'>Your Profile</Header>
                <this.ChangeModal />
                <this.DeleteUserModal />

                <Header as='h2'>Username</Header>
                <Header as='h4'> {this.state.username} </Header>
                <Button content='Change Username' color="yellow" onClick={() => this.setState({
                    modalMode: 'Username'
                })} />
                <Divider />
                <Header as='h2'>Email</Header>
                <Header as='h4'> {this.state.email} </Header>
                <Button content='Change Email' color="yellow" onClick={() => this.setState({
                    modalMode: 'Email'
                })} />
                <Divider />
                <Header as='h2'>Password</Header>
                <Button content='Change Password' color="yellow" onClick={() => this.setState({
                    modalMode: 'Password'
                })} />
                <Divider />
                <Button content='Delete My Account' color="red" onClick={() => this.setState({
                    deleteUser: true
                })} />
            </>
        } else {
            return <>
                <Message
                    header='You are not logged in!'
                    content='Please log in to view your profile.'
                />
            </>
        }
    }


    DeleteUserModal = () => {
        return <Modal
            open={this.state.deleteUser}
        >
            <Modal.Header>DELETE ACCOUNT</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    <Header>Are you sure you want to delete your account?</Header>
                </Modal.Description>
                <Divider hidden/>
                <Form>
                    <Form.Input
                        icon='delete'
                        iconPosition='left'
                        value={this.state.deleteForm}
                        onChange={input => this.setState({ deleteForm: input.target.value })}
                    />
                </Form>
                <Message
                    hidden={!this.state.deleteFormWrong}
                    color={'red'}
                    header='Enter "delete" to confirm.'
                />
            </Modal.Content>
            <Modal.Actions>
                <Button color='black' onClick={() => this.setState({
                    deleteUser: false
                })}>
                    Cancel
                </Button>
                <Button
                    content="Delete my account"
                    labelPosition='right'
                    icon='user delete'
                    onClick={() => this.deleteUser()}
                    color='red'
                />
            </Modal.Actions>
        </Modal>
    }

    ChangeModal = () => {
        if (this.state.modalMode === 'Username') {
            return <Modal
                open={this.state.modalMode === 'Username'}
            >
                <Modal.Header>CHANGE USERNAME</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        <Header>Enter your new Username:</Header>
                    </Modal.Description>
                    <Form>
                        <Form.Input
                            icon='user'
                            iconPosition='left'
                            placeholder='New Username'
                            value={this.state.newUser}
                            onChange={input => this.setState({ newUser: input.target.value })}
                        />
                    </Form>
                    <Message
                        hidden={!this.state.enterUsername}
                        color={'red'}
                        header='Please enter your new username.'
                    />
                    <Message
                        hidden={!this.state.usernameTaken}
                        color={'red'}
                        header='Username already taken.'
                    />
                </Modal.Content>
                <Modal.Actions>
                    <Button color='black' onClick={() => this.setState({
                        modalMode: ''
                    })}>
                        Cancel
                    </Button>
                    <Button
                        content="Change Username"
                        labelPosition='right'
                        icon='checkmark'
                        onClick={() => this.changeUsername()}
                        positive
                    />
                </Modal.Actions>
            </Modal>
        } else if (this.state.modalMode === 'Email') {
            return <Modal
                open={this.state.modalMode === 'Email'}
            >
                <Modal.Header>CHANGE EMAIL</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        <Header>Enter your new Email:</Header>
                    </Modal.Description>
                    <Form>
                        <Form.Input
                            icon='user'
                            iconPosition='left'
                            placeholder='New Email'
                            value={this.state.newEmail}
                            onChange={input => this.setState({ newEmail: input.target.value })}
                        />
                    </Form>
                    <Message
                        hidden={!this.state.enterEmail}
                        color={'red'}
                        header='Please enter your new email.'
                    />
                    <Message
                        hidden={!this.state.emailTaken}
                        color={'red'}
                        header='Email already taken.'
                    />
                    <Message
                        hidden={!this.state.invalidEmail}
                        color={'red'}
                        header='Enter valid email.'
                    />
                </Modal.Content>
                <Modal.Actions>
                    <Button color='black' onClick={() => {
                        this.setState({
                            modalMode: ''
                        })
                    }}>
                        Cancel
                    </Button>
                    <Button
                        content="Change Email"
                        labelPosition='right'
                        icon='checkmark'
                        onClick={() => this.changeEmail()}
                        positive
                    />
                </Modal.Actions>
            </Modal>
        } else if (this.state.modalMode === 'Password') {
            return <Modal
                open={this.state.modalMode === 'Password'}
            >
                <Modal.Header>CHANGE PASSWORD</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        <Header>Enter your new Password:</Header>
                    </Modal.Description>
                    <Form>
                        <Form.Input
                            icon='lock'
                            type='password'
                            iconPosition='left'
                            placeholder='New Password'
                            value={this.state.newPassword}
                            onChange={input => this.setState({ newPassword: input.target.value })}
                        />
                    </Form>
                </Modal.Content>
                <Modal.Content>
                    <Modal.Description>
                        <Header>Confirm new Password:</Header>
                    </Modal.Description>
                    <Form>
                        <Form.Input
                            icon='lock'
                            type='password'
                            iconPosition='left'
                            placeholder='Confirm Password'
                            value={this.state.confirmPassword}
                            onChange={input => this.setState({ confirmPassword: input.target.value })}
                        />
                    </Form>
                    <Message
                        hidden={!this.state.enterPassword}
                        color={'red'}
                        header='Please enter your new password.'
                    />
                    <Message
                        hidden={!this.state.passwordMismatch}
                        color={'red'}
                        header='Passwords do not match.'
                    />
                </Modal.Content>
                <Modal.Actions>
                    <Button color='black' onClick={() => this.setState({
                        modalMode: ''
                    })}>
                        Cancel
                    </Button>
                    <Button
                        content="Change Password"
                        labelPosition='right'
                        icon='checkmark'
                        onClick={() => this.changePassword()}
                        positive
                    />
                </Modal.Actions>
            </Modal>
        } else {
            return <></>
        }
    }

    changeUsername = () => {
        if (this.state.newUser === "") {
            this.setState({ enterUsername: true, usernameTaken: false })
        } else {
            api.put('/users',
                {
                    "u_id": parseInt(localStorage.getItem("userID")),
                    "username": this.state.newUser,
                    "u_email": "",
                    "u_password": "",
                    "isAdmin": ""
                }).then(res => {
                    console.log("Changed Username");
                    localStorage.setItem("username", res.data["Username"]);
                    window.location.reload(false);
                }).catch(error => {
                    if (error.response.data === "Username already taken") {
                        this.setState({ enterUsername: false, usernameTaken: true })
                    }
                    console.log(error.response.data);
                    console.log(error.response.status);
                })
        }
    }

    changeEmail = () => {
        if (this.state.newEmail === "") {
            this.setState({ enterEmail: true, invalidEmail: false, emailTaken: false })
        } else {
            api.put('/users',
                {
                    "u_id": parseInt(localStorage.getItem("userID")),
                    "username": "",
                    "u_email": this.state.newEmail,
                    "u_password": "",
                    "isAdmin": ""
                }).then(res => {
                    console.log("Changed Email");
                    window.location.reload(false);
                }).catch(error => {
                    if (error.response.data === "Enter Valid Email") {
                        this.setState({ enterEmail: false, invalidEmail: true, emailTaken: false })
                    } else if (error.response.data === "Email already taken") {
                        this.setState({ enterEmail: false, invalidEmail: false, emailTaken: true })
                    }
                    console.log(error.response.data);
                    console.log(error.response.status);
                })
        }
    }

    changePassword = () => {
        if (this.state.newPassword === "") {
            this.setState({ enterPassword: true, passwordMismatch: false })
        } else if (this.state.newPassword !== this.state.confirmPassword) {
            this.setState({ enterPassword: false, passwordMismatch: true })
        } else {
            api.put('/users',
                {
                    "u_id": parseInt(localStorage.getItem("userID")),
                    "username": "",
                    "u_email": "",
                    "u_password": this.state.newPassword,
                    "isAdmin": ""
                }).then(res => {
                    console.log("Chaged Password");
                    window.location.reload(false);
                }).catch(error => {
                    console.log(error.response.data);
                    console.log(error.response.status);
                })
        }
    }
}

export default Profile;