var chatApp = new Vue({
    el: '#chatApp',
    data: {
        userData: {
            login: '',
            token: '',
            ID: ''

        },
        groups: [
            {
                ID: 1,
                title: "beka",
                messages: []
            }
        ],

        currentMessage: "", 
        activeGroup: null,
        socket: null
    },
    
    methods: {
        selectGroup: function (group) {
            this.activeGroup = group
        },
        createGroup: function () {
            let groupName = prompt('Podaj nazwę grupy')
        },
        addUserToGroup: function () {
            var users = prompt('Podaj nicki rozdzielone spacją')
            users = users.split(' ')
            axios.post("/add-members", {"member_list": users, "group-ID": this.activeGroup.ID})
            // TODO: check if .then is needed
        },
        sendMessage: function () {
            let message = this.currentMessage
            this.currentMessage = ''
            console.log('sending ' + message )
            this.socket.emit('message', {text: message, groupID: this.activeGroup.ID})
        },
        initSocket() {
            let SELF = this
            namespace = '/chat'

            SELF.socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace)

            SELF.socket.on('connect', function() {
                console.log('connected')
                SELF.socket.emit('auth', {token: SELF.userData.token, ID: SELF.userData.ID});
                
            });

            SELF.socket.on('message', function(message) {
                console.log('message recived: ')
                console.log(message)
                
                let userID = message['userID']                
                let messageBody = message['text']
                let groupID = message['groupID']
                
                SELF.groups.forEach(group => {
                    console.log(group)
                    if (groupID == group['ID']) {
                        console.log("if chyba zachodzi")
                        group.messages.push(
                            {
                                author: userID,
                                text: messageBody 
                            }
                        )
                    }
                
                }); 
            });

            SELF.socket.on('auth_success', function(messages) {
                
                if(messages.status == 'fail') {
                    window.location = '/login'
                }

                console.log('login successful')
                
            });
        }
        
    },

    created: function () {
        this.activeGroup = this.groups[0]
        this.userData.token = localStorage.getItem('token')
        this.userData.login = localStorage.getItem('login')
        this.userData.ID = localStorage.getItem('ID')

        this.initSocket()
    }
})

