
# Nagios alerts on WhatsApp through D7 Connector
## Subscribe to D7WhatsApp and create templates
Before starting nagios setup make sure you have a valid WhatsApp subscription on https://d7networks.com.
Please contact support@d7networks.com or signup at https://d7networks.com to enable WhatsApp on your D7 Account. 

Once the whatsapp account is registered with meta, You will have to create following two templates for notifications. 

Template name: **host_notification_1**

Body: 

    ***** Nagios *****
    Notification Type: {{1}}
    Host: {{2}}
    State: {{3}}
    Address: {{4}}
    Info: {{5}}
    Date/Time: {{6}}
    
    This alert was generated by Nagios


Template name: **service_notification_1**

Body: 

    ***** Nagios *****
    Notification Type: {{1}}
    Service: {{2}}
    Host: {{3}}
    Address: {{4}}
    State: {{5}}
    Date/Time: {{6}}
    Additional Info:{{7}}
    
    This alert was generated by Nagios

Once these templates are approved by Meta, you can continue with the configurations. 

## Configure Nagios


### 1. Copy python scripts
Copy **d7whatsapp_service.py** and **d7whatsapp_host.py** python script files to your Nagios plugins folder and make it executable. 
You can download it from https://github.com/d7networks/d7whatsapp-nagios

Following are the location of plugins folder in different Operating Systems.

    Debian/Ubuntu: /usr/local/nagios/libexec
    Centos: /usr/lib/nagios/plugins (32 bit)
    /usr/lib64/nagios/plugins (64 bit)

### 2. Create commands for WhatsApp Host and service notifications. 
Make sure to replace **SOURCE_NUMBER** with the number you've registered with D7WhatsApp. 

    #define command{
           command_name    host-notify-by-whatsapp
           command_line    $USER1$/d7whatsapp_host.py --source_address "SOURCE_NUMBER" --to $CONTACTPAGER$ --template_id "host_notification_1"  --type "$NOTIFICATIONTYPE$" --host "$HOSTNAME$" --address "$HOSTADDRESS$" --state "$HOSTSTATE$" --date "$LONGDATETIME$" --info "$HOSTOUTPUT$"
           }
    
    #define command{
     command_name    service-notify-by-whatsapp
           command_line    $USER1$/d7whatsapp_service.py --source_address "SOURCE_NUMBER" --to $CONTACTPAGER$ --template_id "service_notification_1" --type "$NOTIFICATIONTYPE$" --service "$SERVICEDESC$" --host "$HOSTNAME$" --address "$HOSTADDRESS$" --state "$SERVICESTATE$" --date "$LONGDATETIME$" --info "$SERVICEOUTPUT$"
     }

### 3. Update contact template
Update service_notification_commands and  add host_notification_commands and include whatsapp notification commands

Default path : 
/usr/local/nagios/etc/objects/contacts.cfg 
or 
/usr/local/nagios/etc/objects/templates.cfg

    define contact{
            name                            generic-contact
            service_notification_period     24x7
            host_notification_period        24x7
            service_notification_options    w,u,c,r,f,s
            host_notification_options       d,u,r,f,s
            service_notification_commands   notify-service-by-email,service-notify-by-whatsapp
            host_notification_commands      notify-host-by-email,host-notify-by-whatsapp
            register                        0
            }


### 4. Add a pager number
   Add pager number to your contacts, make sure it has the international prefix

       define contact {
           contact_name            nagiosadmin
           use                     generic-contact
           alias                   Nagios Admin
           email                   support@d7networks.com
           pager                   +97150975xxxx
       }

### 5. Support and Help

For all queries and help on installation please contact support@d7networks.com or visit https://d7networks.com
################################################################
