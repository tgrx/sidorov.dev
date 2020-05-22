# def sync(self, force: bool = False) -> None:
#     if not self.ical_url:
#         self.synced = False
#         self.save()
#         return
#
#     atm = datetime.utcnow().astimezone(pytz.UTC)
#     next_sync_time = self.get_next_sync() if not force else atm
#
#     # if (next_sync_time - atm).total_seconds() > 5:  # FIXME: magic
#     #     return
#
#     ical = self.download_ical()
#     if not ical:
#         self.synced_at = atm
#         self.synced = False
#         self.save()
#         return
#
#     self.ical = ical
#     self.synced_at = atm
#     self.synced = True
#     self.save()
#
# def get_next_sync(self) -> datetime:
#     if self.synced_at:
#         return self.synced_at + timedelta(minutes=5)  # FIXME: magic
#     return datetime.utcnow().astimezone(pytz.UTC)
#
# @safe
# def download_ical(self) -> Union[str, None]:
#     if not self.ical_url:
#         return None
#
#     resp = requests.get(self.ical_url)
#     if resp.status_code != 200:
#         return None
#
#     return resp.content.decode()
