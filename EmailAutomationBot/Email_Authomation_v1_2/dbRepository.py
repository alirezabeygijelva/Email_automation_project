import datetime
from ..models import Email, TelegramGroup, TelegramBot, MailServerAuthenticationInfo, BotGroupEmailUserRelations, LastEmailDateTimeRead,ActivateTelegramBots
import datetime


class DataBaseRepository:
    def getdata():
        pass

    def setdata():
        pass


class repositoryDataForFinixmail(DataBaseRepository):
    def getdata(self):
        relations_info = BotGroupEmailUserRelations.objects.values_list()
        self.info_list = []
        for i in relations_info:
            self.inner_list = []
            auth_info = MailServerAuthenticationInfo.objects.filter(pk=i[4]).values_list(

                "tenant_id", "client_id", "secret", "authority", "scope")
            group_info = TelegramGroup.objects.filter(
                pk=i[2]).values_list("group_id")
            bot_info = TelegramBot.objects.filter(
                pk=i[3]).values_list("bot_token")
            self.email_addr = i[1]
            self.SCOPE = []
            self.SCOPE.append(auth_info[0][4].strip('"'))
            self.TENANT_ID, self.CLIENT_ID, self.SECRET, self.AUTHORITY, self.bot_token, self.group_id = auth_info[
                0][0], auth_info[0][1], auth_info[0][2], auth_info[0][3], bot_info[0][0], group_info[0][0]
            self.AUTHORITY = f"{self.AUTHORITY}{self.TENANT_ID}"
            self.inner_list.append(self.TENANT_ID)  # 0
            self.inner_list.append(self.CLIENT_ID)  # 1
            self.inner_list.append(self.SECRET)  # 2
            self.inner_list.append(self.AUTHORITY)  # 3
            self.inner_list.append(self.SCOPE)  # 4
            self.inner_list.append(self.bot_token)  # 5
            self.inner_list.append(self.group_id)  # 6
            self.inner_list.append(self.email_addr)  # 7
            self.info_list.append(self.inner_list)
        return self.info_list


class GetAuthenticationInfoOfSelectedEmail(DataBaseRepository):
    def getdata(self, selected_mail):
        pass


class LastMailRead(DataBaseRepository):
    def getdata(self, email_addr):

        last_email_datetime = LastEmailDateTimeRead.objects.filter(
            email_address=email_addr).values('lastemailreaddatetime').first()
        if last_email_datetime:
            formatted_datetime = last_email_datetime['lastemailreaddatetime'].isoformat(
            )
            formatted_datetime = formatted_datetime[:-6]
            formatted_datetime = formatted_datetime + "Z"
            return formatted_datetime

    def setdata(self, email_addr, time):
        email_instance = Email.objects.get(email_address=email_addr)
        current_time = datetime.datetime.now()
        current_time = str(current_time)
        current_time = current_time[:-6]
        current_time = current_time+"Z"

        last_email_datetime, created = LastEmailDateTimeRead.objects.update_or_create(
            email_address=email_instance,
            defaults={'lastemailreaddatetime': current_time}
        )

        return


class GetGroupsListForBot(DataBaseRepository):
    def getdata(self, bot_token):
        self.bot_token = bot_token
        groupsforbot = BotGroupEmalUserRelations.objects.filter(
            bot_id=self.bot_token).values_list("email_address")
        return groupsforbot


# this class give mail's list data to the bot
class GetMailsToBot(DataBaseRepository):
    def getdata(self, bot_token, group_id):
        self.bot_token = bot_token
        self.group_id = group_id
        mails_for_bot = BotGroupEmalUserRelations.objects.filter(
            bot_id=bot_token, group_id=group_id).values_list("email_address")
        return mails_for_bot

class GetGroupList(DataBaseRepository):
    def getdata(self, bot_token):
        result_queryset = BotGroupEmailUserRelations.objects.filter(
        bot_id=bot_token).values('group_id')
    
        _list = []
        for _ in result_queryset:
            _list.append(int(_['group_id']))
        return _list
    
class GetMailsList(DataBaseRepository):
    def getdata(self,bot_token, group_id):
        result_queryset = BotGroupEmailUserRelations.objects.filter(
        bot_id=bot_token, group_id=group_id).values('email_address')
        _list = []
        for _ in result_queryset:
            _list.append(_["email_address"])
        return _list


class CheckBotIsActive(DataBaseRepository):
    def getdata(self,bot_token):
        self.bot_token = bot_token
        # bot = ActivateTelegramBots.objects.filter(bot_token=self.bot_token).values_list('status')
        bot = ActivateTelegramBots.objects.filter(bot_token=self.bot_token).values("status")
        
        if bot.exists() and bot[0]['status'] == "active":
            return True
        else:
            return False