import datetime


def release_reserved(item):
    # Release the item (note that works in any session)
    item.reserved_until = None
    item.reserved_by = None
    item.reserved_session = ""
    item.save()


def reserve(item, user, session):
    ret = True

    if not item.reserved:
        # Make reservation
        # ret:true = is now reserved
        # ret:false = somebody got there before user
        item.reserved_until = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        item.reserved_by = user
        item.reserved_session = session.session_key
        item.save()
    else:
        # Cancel reservation
        # ret: false = reserved -> free | free -> free
        # ret: true = Not reserved by user
        if item.reserved_by.id == user.id:
            release_reserved(item)
            ret = False
    return ret


def item_on_loan(item):
    from lending.models import LentItems
    return LentItems.objects.filter(item=item).exclude(item__lentitems__return_dt__isnull=False).count > 0


def items_on_loan():
    from lending.models import LentItems
    lent_items = LentItems.objects.filter(return_dt__isnull=True)
    for item in lent_items:
        yield item.item
