# -*- coding: utf-8 -*-
#
#   Copyright © 2011-2013 APINC Devel Team
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

import os
import sys
from optparse import make_option

from datetime import date, datetime
import pytz
import crypt

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site

import apm.apps.groups.models as groups
import apm.apps.members.models as members
import apm.apps.news.models as news
import apm.apps.pages.models as pages
#import apm.apps.subscriptions.models as subscriptions

PSEUDO_STATIC_PAGES = [
    ("homepage", "Bienvenue !"),
    ("about", "About page title"),
    ("legal-notice", "Legal notice and terms of use"),
    ("contact", "Contact page title"),
    ("association", "The association"),
    ("status", "Statuts de l'association"),
    ("rules", "Charte d'utilisation des services"),
]

class Command(BaseCommand):
    help = 'Fill the database with initial data.'
    option_list = BaseCommand.option_list + (
            make_option('--development', action='store_true',
                dest='development', default=False,
                help='Load development data into the database.'),
            )

    def handle(self, *args, **options):
        # cette partie regroupe les données des pages pseudos-statiques
        try:
            # initializing pseudo-static pages
            for slug, title in PSEUDO_STATIC_PAGES:
                pseudo_static_page = pages.TextBlock(slug=slug, title=title)
                pseudo_static_page.save()
                self.stdout.write("Pseudo-static page '%s' inserted.\n" % slug)

        except Exception, e:
            # TODO Error message handling
            raise CommandError('Filldb pseudo-static pages "%s"' % e)

        if options.get('development', False):
            # Cette partie regroupe les valeurs fixes de la base,
            # que l'on s'autorise donc à tester en dur dans le code.
            # Merci d'y ajouter tous les champs que vous devez tester en dur.

            msg = """\nVoulez-vous remplir la base de donnée avec des data de test (oui/non) ? """
            confirm = raw_input(msg)
            while 1:
                if confirm not in ('oui', 'non'):
                    confirm = raw_input('Merci de saisir "oui" ou "non" : ')
                    continue
                break

            if confirm == 'non':
                sys.exit(0)

            try:
                # apinc roles
                #role_admin = members.Role(name='Administrateur', rank = 10)
                #role_admin.save()
                #self.stdout.write("\nRole 'administrateur' inserted.\n")
                role_president = members.Role(name='President', rank = 30)
                role_president.save()
                self.stdout.write("Role 'président' inserted.\n")
                role_vice_president = members.Role(name='Vice-president', rank = 40)
                role_vice_president.save()
                self.stdout.write("Role 'vice-président' inserted.\n")
                role_tresorier = members.Role(name='Tresorier', rank = 50)
                role_tresorier.save()
                self.stdout.write("Role 'trésorier' inserted.\n")
                role_tresorier_adjoint = members.Role(name='Tresorier adjoint', rank = 60)
                role_tresorier_adjoint.save()
                self.stdout.write("Role 'trésorier adjoint' inserted.\n")
                role_secretaire = members.Role(name='Secretaire', rank = 70)
                role_secretaire.save()
                self.stdout.write("Role 'secrétaire' inserted.\n")
                role_secretaire_adjoint = members.Role(name='Secretaire adjoint', rank = 80)
                role_secretaire_adjoint.save()
                self.stdout.write("Role 'secrétaire adjoint' inserted.\n")
                #role_membre_bureau = members.Role(name='Membre du bureau', rank = 90)
                #role_membre_bureau.save()
                #self.stdout.write("Role 'membre du bureau' inserted.\n")
                #role_membre = members.Role(name='Membre', rank = 100)
                #role_membre.save()
                #self.stdout.write("Role 'membre' inserted.\n")
                #role_demandeur = members.Role(name='Demandeur', rank = 110)
                #role_demandeur.save()
                #self.stdout.write("Role 'demandeur' inserted.\n")

                # apinc groups
                apinc_admin = groups.Group(name='apinc-admin', slug='apinc-admin')
                apinc_admin.email = "a-admin@a.org"
                apinc_admin.save()
                self.stdout.write("Group 'apinc-admin' inserted.\n")
                apinc_devel = groups.Group(name='apinc-devel', slug='apinc-devel')
                apinc_devel.email = "a-devel@a.org"
                apinc_devel.save()
                self.stdout.write("Group 'apinc-devel' inserted.\n")
                apinc_bureau = groups.Group(name='apinc-bureau', slug='apinc-bureau')
                apinc_bureau.email = "a-bureau@a.org"
                apinc_bureau.save()
                self.stdout.write("Group 'apinc-bureau' inserted.\n")
                apinc_secretariat = groups.Group(name='apinc-secretariat', slug='apinc-secretariat')
                apinc_secretariat.email = "a-secretariat@a.org"
                apinc_secretariat.save()
                self.stdout.write("Group 'apinc-secretariat' inserted.\n")
                apinc_tresorier = groups.Group(name='apinc-tresorier', slug='apinc-tresorier')
                apinc_tresorier.email = "a-tresorier@a.org"
                apinc_tresorier.save()
                self.stdout.write("Group 'apinc-tresorier' inserted.\n")
                apinc_contrib = groups.Group(name='apinc-contributeur', slug='apinc-contributeur')
                apinc_contrib.email = "a-contrib@a.org"
                apinc_contrib.save()
                self.stdout.write("Group 'apinc-contributeur' inserted.\n")
                apinc_membre = groups.Group(name='apinc-membre', slug='apinc-member')
                apinc_membre.email = "a-membre@a.org"
                apinc_membre.save()
                self.stdout.write("Group 'apinc-membre' inserted.\n")

                # Persons
                laurent = members.Person(username="laurent", email="lau@a.org",
                        first_name="Laurent", last_name="Bives", sex="M",
                        is_staff=True, is_superuser=True)
                laurent.birth_date = date(1988,03,20)
                laurent.set_password(crypt.crypt("laurent", "laurent"))
                laurent.save()

                apinc_admin.add(laurent)
                apinc_devel.add(laurent)
                apinc_bureau.add(laurent)

                laurent_private = members.PersonPrivate()
                laurent_private.person = laurent
                laurent_private.notes = "Donnees privees accessibles seulement par les admins ou le secretariat apinc."
                laurent_private.save()

                self.stdout.write("Membre 'laurent' inserted.\n")

                gm = groups.GroupMembership(start_date=date(2010,1,1), end_date=date(2011,1,1))
                gm.group = apinc_tresorier
                gm.member = laurent
                gm.save()

                self.stdout.write("Membership 'apinc-tresorier' to 'laurent' inserted.\n")

                contributeur = members.Person.objects.create_user("contributeur", "cont@ribu.ter", crypt.crypt("contributeur", "contributeur"))
                contributeur.is_staff = True
                contributeur.is_superuser = True
                contributeur.first_name = "Contrib"
                contributeur.last_name = "Uter"
                contributeur.sex = 'F'
                contributeur.birth_date = date(1961,11,10)
                contributeur.save()

                contributeur_private = members.PersonPrivate()
                contributeur_private.person = contributeur
                contributeur_private.notes = "Donnees privees du membre 'contributeur' accessibles seulement par les admins ou le secretariat apinc."
                contributeur_private.save()
                self.stdout.write("Membre 'contributeur' (generic) inserted.\n")

                apinc_contrib.add(contributeur)
                self.stdout.write("Membre 'contributeur' joins 'apinc_contrib' group.\n")

                misric = members.Person.objects.create_user("misric", "m@sric.cc", crypt.crypt("misric", "misric"))
                misric.is_staff = True
                misric.is_superuser = True
                misric.first_name = "Misric"
                misric.last_name = "Msrc"
                misric.sex = 'M'
                misric.birth_date = date(1961,11,10)
                misric.save()

                misric_private = members.PersonPrivate()
                misric_private.person = misric
                misric_private.notes = "Donnees privees du membre 'misric' accessibles seulement par les admins ou le secretariat apinc."
                misric_private.save()
                self.stdout.write("Membre 'misric' (generic) inserted.\n")

                apinc_contrib.add(misric)
                self.stdout.write("Membre 'misric' joins 'apinc_contrib' group.\n")

                # news
                news1 = news.News()
                news1.status = 1
                news1.body_html = "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lacinia \r\nvestibulum mollis. Sed non tempor est. Vestibulum vel mauris massa, ac \r\nhendrerit est. Integer scelerisque, ante at ultricies elementum, risus \r\norci bibendum arcu, non porta nisl diam in sapien. Vestibulum vitae sem a\r\n diam aliquam volutpat posuere non nisi. Nullam faucibus, neque id \r\nrutrum aliquam, nibh lorem condimentum dui, consequat lacinia ligula \r\nnisl ullamcorper nulla. In hac habitasse platea dictumst. Aliquam \r\nvulputate interdum eros, vitae eleifend mauris tincidunt sed. In vel \r\ntortor quis libero aliquet tempor eget in arcu. Ut sed neque quam. \r\nVivamus condimentum felis et justo vestibulum varius. Praesent egestas \r\ntincidunt leo, sed dictum metus vestibulum quis. Vestibulum sodales \r\nposuere aliquet. Vivamus suscipit nunc eu sem pulvinar volutpat. Nunc \r\nnon dui non enim tempor varius. Cum sociis natoque penatibus et magnis \r\ndis parturient montes, nascetur ridiculus mus. In eget urna id enim \r\niaculis elementum posuere nec mi. Curabitur a fringilla odio.</p>Ut vel dolor eget lectus tempus tempor in posuere mi. Sed purus ipsum, \r\nfringilla vel ullamcorper aliquet, iaculis non mi. Cras mi diam, \r\nultrices eget luctus non, congue eget nibh. Pellentesque vitae felis \r\nmetus, sed auctor dui. Nulla eget sem ligula. Cras sollicitudin eleifend\r\n lacus varius egestas. Pellentesque volutpat laoreet felis, porttitor \r\nconsectetur sem accumsan ut. Sed accumsan sem non mi suscipit molestie. \r\nFusce auctor tincidunt elit. Phasellus ut velit laoreet est sagittis \r\nvarius in et nunc. Proin scelerisque nisi eget orci sodales sit amet \r\ninterdum nulla tempus. Sed rutrum metus vel odio scelerisque eleifend. \r\nDuis nec libero elit. Donec non lorem ante. Suspendisse sagittis laoreet\r\n pulvinar. Nullam a eros id justo vestibulum aliquet viverra cursus \r\nvelit. Nam at malesuada purus.\r\n"
                news1.pub_date = datetime(2011,06,23,13,24,57,tzinfo=pytz.utc)
                #news1.slug = "nam-pulvinar-malesuada-dictum-nunc"
                news1.title = "Nàm éçapulvinar malesuada dictum. Nunc."
                news1.save()
                self.stdout.write("News 1 inserted.\n")

                news2 = news.News()
                news2.status = 1
                news2.body_html = "<p>Nullam eget pharetra elit. Nam convallis scelerisque lorem ac volutpat. \r\nDonec vulputate orci accumsan urna iaculis blandit scelerisque est \r\ndictum. Nunc non nunc eros. Suspendisse ultricies felis et lorem gravida\r\n rhoncus. Ut euismod pulvinar mauris, eget lobortis quam ultrices et. \r\nDonec porttitor urna purus, ut varius sapien. Cras aliquet diam a lacus \r\nconsequat eleifend. Ut vel nisl odio. Cras nec risus ac ante mattis \r\ntempor. Cras malesuada mattis nisi, sit amet vehicula tellus ornare \r\nquis. In imperdiet mauris eu tellus convallis a eleifend neque posuere. \r\nNulla facilisis, lacus ut mollis auctor, neque sapien hendrerit elit, \r\neleifend euismod lacus tellus quis eros. Maecenas dui mi, pellentesque \r\nfeugiat feugiat vel, commodo id quam. Donec ornare iaculis augue id \r\nmalesuada. Aenean mattis condimentum mi ac porttitor. Fusce ultricies \r\ncursus viverra. Donec scelerisque tellus fringilla urna ornare sit amet \r\ntempor mauris ultrices.\r\n</p><ul><li>Cras luctus turpis at turpis euismod fringilla.</li><li>Integer et sapien eget est dignissim vulputate imperdiet eu neque.</li><li>Curabitur in tellus ligula, eget gravida mi.</li><li>Donec vel libero at quam gravida placerat.</li></ul>\r\n<p>\r\nProin feugiat nibh sed arcu lobortis ut varius diam feugiat. Suspendisse\r\n potenti. Maecenas convallis elit eget ligula scelerisque molestie. \r\nEtiam a sapien libero. Fusce vestibulum interdum lectus, in condimentum \r\nlibero placerat vel. Sed sit amet erat vitae neque venenatis pretium nec\r\n eu nisl. Praesent tempus est in justo pellentesque rhoncus. Nulla \r\nlaoreet metus id mauris feugiat vel aliquam metus pharetra. Phasellus \r\nmollis elementum turpis gravida ultricies. Sed tempus sollicitudin \r\nblandit. Nunc auctor dapibus ligula et scelerisque. Duis iaculis arcu \r\nnec purus molestie at tincidunt nisl fermentum. Vivamus eget vehicula \r\nmetus. Sed tincidunt arcu eu diam semper facilisis. Proin vitae dolor a \r\nodio pulvinar rutrum vitae a augue. Quisque semper facilisis mattis. \r\nDonec convallis facilisis justo, vel scelerisque est mattis eget. Sed \r\ncondimentum nibh id odio dignissim at tincidunt mi dapibus.\r\n</p>"
                news2.pub_date = datetime(2011,05,8,12,0,21,tzinfo=pytz.utc)
                news2.slug = "aadipiscing-ultrices-vel-vel-massa"
                news2.title = "Aadipiscing ultrices vel vel massa"
                news2.save()
                self.stdout.write("News 2 inserted.\n")

                news3 = news.News()
                news3.status = 1
                news3.body_html = "<p>Phasellus ut magna velit. Pellentesque luctus metus id justo ullamcorper\r\n fringilla. Aenean scelerisque malesuada augue, in pulvinar diam pretium\r\n vel metus. </p><h3>Fusce enim massa</h3><p>Luctus a adipiscing at, viverra malesuada lorem. \r\nInteger viverra, nisi scelerisque volutpat varius, elit diam auctor \r\nmassa, quis venenatis eros orci vel felis. Donec sagittis lobortis \r\naugue, scelerisque posuere massa feugiat quis. Praesent suscipit dolor \r\nnon eros faucibus sagittis. Vestibulum vitae pellentesque eros. Morbi \r\nbibendum mauris eu erat rutrum molestie. Phasellus elementum pharetra \r\nnulla eget sollicitudin. Proin hendrerit ornare elit, eu cursus augue \r\nvestibulum sed. Cras eget purus at nisl viverra vestibulum id convallis \r\nquam. Quisque ornare justo nec ligula consequat tristique. Curabitur \r\nconvallis pulvinar ante ac auctor. In mattis varius massa, eget commodo \r\nipsum imperdiet vel. Integer vulputate scelerisque lorem, id tincidunt \r\nelit congue ut.</p>"
                news3.pub_date = datetime(2011,05,2,8,13,02,tzinfo=pytz.utc)
                news3.slug = "nam-convallis"
                news3.title = "Nam convallis"
                news3.save()
                self.stdout.write("News 3 inserted.\n")

                news4 = news.News()
                news4.status = 1
                news4.body_html = "<h3>Vestibulum neque velit</h3><ul><li>Lobortis ut iaculis ut</li><li>Mollis nec turpis</li><li>Nulla\r\n a porta nisl.</li></ul><p>Nullam iaculis fringilla consequat. Aenean vel justo sit \r\namet leo semper ultrices et sit amet lorem. Ut ac dolor in massa \r\nultricies euismod non sit amet ligula. Nulla <strong>metus</strong> felis, placerat in \r\nsagittis eu, rhoncus sit amet risus. In eget <strong>lorem</strong> justo. Curabitur \r\nbibendum tristique enim, vel dapibus enim vehicula vel. In ornare \r\nlacinia lacus eget blandit. Ut<sup>id</sup> metus id velit interdum cursus. Nunc \r\nrutrum viverra nisl, eu elementum odio bibendum eget.&#160;\r\n  \r\n</p>"
                news4.pub_date = datetime(2011,04,18,13,24,11,tzinfo=pytz.utc)
                news4.slug = "pellentesque-vestibulum-mattis-feugiat"
                news4.title = "Pellentesque vestibulum mattis feugiat"
                news4.save()
                self.stdout.write("News 4 inserted.\n")

                news5 = news.News()
                news5.status = 1
                news5.body_html = "<p><em>Morbi tellus risus</em>, euismod at pulvinar eget, interdum vel dolor. Aenean\r\n dictum condimentum interdum. Etiam a erat massa. Sed fermentum porta \r\nconvallis. <strong>Nam eget dolor in magna porta sagittis id sed elit.</strong> Fusce \r\nlaoreet massa diam, in placerat ipsum. Donec pharetra tempus convallis. \r\nAenean sit amet dolor ante, sit amet fringilla ligula. Mauris porta, \r\nlectus ac lobortis tincidunt, mauris lacus laoreet est, vitae cursus \r\nfelis lacus a elit. Pellentesque ut purus et augue hendrerit aliquam et \r\nsit amet est. </p><blockquote><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur \r\nsuscipit posuere purus, vel tempus turpis aliquet id.</p></blockquote>"
                news5.pub_date = datetime(2011,04,14,4,54,17,tzinfo=pytz.utc)
                news5.slug = "morbi-tellus-risus"
                news5.title = "Morbi tellus risus"
                news5.save()
                self.stdout.write("News 5 inserted.\n")

                news6 = news.News()
                news6.status = 0 
                news6.body_html = "<div><h2>Neque porro quisquam</h2><ol><li>Sed eget massa condimentum justo pellentesque gravida.</li><li>Aliquam lobortis eros non justo aliquam sed cursus turpis porta.</li><li>Donec tincidunt aliquet dolor, vel tempus est hendrerit eget.</li></ol><h3><em>est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...</em></h3></div>"
                news6.pub_date = datetime(2010,02,15,9,35,02,tzinfo=pytz.utc)
                news6.slug = "neque-porro-quisquam"
                news6.title = "Neque porro quisquam"
                news6.save()
                self.stdout.write("News 6 inserted.\n")

                news7 = news.News()
                news7.status = 1
                news7.body_html = "<div><h2>Lorem ipsum</h2><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam id hendrerit mi. Vivamus placerat turpis non turpis commodo posuere. <strong>Vivamus</strong> cursus bibendum iaculis. In rutrum sem non lorem malesuada in gravida leo adipiscing. Nullam ultrices bibendum pretium. Aenean condimentum, ipsum et imperdiet fringilla, magna ipsum interdum ligula, eget condimentum lacus tellus a leo. Curabitur imperdiet consequat nulla, sed rhoncus eros porttitor a. Pellentesque vel purus ut neque vehicula mollis sed ut metus. Ut interdum aliquet blandit. In urna eros, sollicitudin eu eleifend ac, mollis nec lectus. In interdum pretium <strong>venenatis</strong>. Vestibulum venenatis, risus sed rutrum elementum, justo leo gravida purus, id porttitor est tellus sed ante. Maecenas et dapibus dolor. Curabitur pulvinar, leo nec imperdiet porttitor, odio quam gravida lacus, vitae tincidunt dolor neque ut enim. In <sup>gravida</sup>, nibh ut molestie sagittis, arcu sem laoreet quam, in vehicula quam neque a risus.</p><h2>Ut interdum aliquet blandit</span></h2></div></span><div></span><div><ul><li>In eu quam et tortor mollis facilisis ut varius ipsum.</li><li>Quisque condimentum porta nibh, in congue nulla iaculis eu.</li></ul><h3>Quisque dignissim scelerisque felis, sit amet tempor justo vehicula eget.</span></h3><ul><li>Phasellus non justo neque, quis mollis lorem.</li><li>Maecenas vehicula iaculis elit, nec tempor urna elementum bibendum.</li></ul><p>Suspendisse nec mi diam, a viverra ligula. Quisque iaculis arcu eu lectus egestas malesuada egestas ac eros. Maecenas dignissim quam tincidunt quam tincidunt et tincidunt orci malesuada. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse at ante ligula, in interdum erat. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.</p><blockquote><p>Sed id lacus nibh, ac dictum nisi. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sit amet lorem et lorem suscipit ultricies venenatis non justo. Aenean cursus facilisis elit a feugiat. Mauris lacus diam, convallis et vulputate ut, dapibus eu lectus. In arcu quam, pharetra in egestas vitae, ultrices et urna. Nunc lobortis bibendum diam vitae venenatis. Ut scelerisque, risus sit amet tincidunt placerat, sapien massa ultricies odio, ut blandit lectus nulla eget neque.</p></blockquote></div></span></div>"
                news7.pub_date = datetime(2010,9,07,22,00,32,tzinfo=pytz.utc)
                news7.slug = "vivamus-cursus-bibendum-iaculis"
                news7.title = "Vivamus cursus bibendum iaculis"
                news7.save()
                self.stdout.write("News 7 inserted.\n")

                news8 = news.News()
                news8.status = 0 
                news8.body_html = "Vivamus vehicula feugiat lacus id sagittis. Phasellus venenatis vulputate velit non pellentesque. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse nisi enim, scelerisque at ullamcorper id, pharetra id magna. Suspendisse augue neque, faucibus nec interdum vitae, lacinia quis justo. Nullam a magna mi. Etiam hendrerit diam ut ipsum dignissim lacinia. Fusce porttitor erat eu urna porta ac tempor sapien ullamcorper. Aliquam magna massa, placerat at imperdiet at, volutpat consectetur lectus. Nulla iaculis adipiscing commodo. Pellentesque eu purus volutpat felis suscipit porttitor. In dapibus, ligula molestie fringilla posuere, mi leo laoreet enim, vitae congue purus nisl vel diam. Ut tempus sapien lacinia neque viverra at commodo orci interdum. Vivamus pellentesque pellentesque scelerisque. Mauris varius varius velit eget fermentum. Duis auctor tortor eu dui dignissim porta."
                news8.pub_date = datetime(2011,01,13,23,12,37,tzinfo=pytz.utc)
                news8.slug = "vivamus-vehicula"
                news8.title = "Vivamus vehicula"
                news8.save()
                self.stdout.write("News 8 inserted.\n")

                self.stdout.write('Successfully filled database\n')

            except Exception, e:
                # TODO Error message handling
                raise CommandError('Filldb development data "%s"' % e)
