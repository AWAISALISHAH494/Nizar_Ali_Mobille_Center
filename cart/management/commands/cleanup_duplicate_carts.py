from django.core.management.base import BaseCommand
from django.db import transaction
from cart.models import Cart, CartItem


class Command(BaseCommand):
    help = 'Clean up duplicate carts by merging them and keeping the most recent one'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        # Find duplicate carts for authenticated users
        user_carts = {}
        for cart in Cart.objects.filter(user__isnull=False):
            user_id = cart.user_id
            if user_id not in user_carts:
                user_carts[user_id] = []
            user_carts[user_id].append(cart)
        
        # Find duplicate carts for sessions
        session_carts = {}
        for cart in Cart.objects.filter(session_key__isnull=False):
            session_key = cart.session_key
            if session_key not in session_carts:
                session_carts[session_key] = []
            session_carts[session_key].append(cart)
        
        total_merged = 0
        total_items_moved = 0
        
        # Process user carts
        for user_id, carts in user_carts.items():
            if len(carts) > 1:
                self.stdout.write(f'Found {len(carts)} carts for user {user_id}')
                
                # Sort by created_at, keep the most recent
                carts.sort(key=lambda x: x.created_at, reverse=True)
                keep_cart = carts[0]
                merge_carts = carts[1:]
                
                if not dry_run:
                    with transaction.atomic():
                        for cart in merge_carts:
                            # Move all items to the cart we're keeping
                            for item in cart.items.all():
                                item.cart = keep_cart
                                item.save()
                                total_items_moved += 1
                            
                            # Delete the duplicate cart
                            cart.delete()
                            total_merged += 1
                else:
                    total_merged += len(merge_carts)
                    for cart in merge_carts:
                        total_items_moved += cart.items.count()
        
        # Process session carts
        for session_key, carts in session_carts.items():
            if len(carts) > 1:
                self.stdout.write(f'Found {len(carts)} carts for session {session_key}')
                
                # Sort by created_at, keep the most recent
                carts.sort(key=lambda x: x.created_at, reverse=True)
                keep_cart = carts[0]
                merge_carts = carts[1:]
                
                if not dry_run:
                    with transaction.atomic():
                        for cart in merge_carts:
                            # Move all items to the cart we're keeping
                            for item in cart.items.all():
                                item.cart = keep_cart
                                item.save()
                                total_items_moved += 1
                            
                            # Delete the duplicate cart
                            cart.delete()
                            total_merged += 1
                else:
                    total_merged += len(merge_carts)
                    for cart in merge_carts:
                        total_items_moved += cart.items.count()
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Would merge {total_merged} duplicate carts and move {total_items_moved} items'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully merged {total_merged} duplicate carts and moved {total_items_moved} items'
                )
            )
