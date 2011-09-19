# -*- coding: utf-8
"""
apinc/manage/management/commands/filldb.py
"""
#
#   Copyright © 2011 APINC Devel Team
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
#

import os
import sys

from datetime import date, datetime


from django.core.management.base import NoArgsCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

import apinc.groups.models as groups
import apinc.members.models as members
import apinc.news.models as news
import apinc.pages.models as pages


class Command(NoArgsCommand):
    help = 'Fill the database with initial data for dev purpose.'

    def handle_noargs(self, *args, **options):

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
            # apinc pseudo-static pages
            homepage = pages.TextBlock(slug="homepage", title="Bienvenue !")
            homepage.body_html = "<p><strong>L'association APINC propose depuis décembre 2001 des services non commerciaux autogérés, administrés par des bénévoles et destinés aux projets non marchands.</strong></p><p>L'ensemble des membres agit sur les décisions concernant la vie de l'association et participe à la vie de la communauté. L'association rassemble des Internautes qui partagent des idées communes : développer, défendre et promouvoir l'Internet non commercial et le partage des connaissances !</p></span>"
            homepage.save()
            self.stdout.write("homepage pseudo-static page inserted.\n")

            about = pages.TextBlock(slug="about", title="About page title")
            about.body_html = "Contenu de la page à propos."
            about.save()
            self.stdout.write("About pseudo-static page inserted.\n")

            legal_notice = pages.TextBlock(slug="legal-notice", title="Legal notice and terms of use")
            legal_notice.body_html = " <p>L'Association pour la promotion de l'Internet Non Commercial est une association de loi 1901.</p>\r\n<h3>Siège social</h3><p>Association APINC - Federation Française des Clubs Unesco<br />173 rue de Charenton<br />75012 PARIS<br />FRANCE</p>"
            legal_notice.save()
            self.stdout.write("Legal notice pseudo-static page inserted.\n")

            contact = pages.TextBlock(slug="contact", title="Contact page title")
            contact.body_html = "Contenu de la page des contacts."
            contact.save()
            self.stdout.write("Contact pseudo-static page inserted.\n")

            # apinc roles
            role1 = members.Role(name='Administrateur', rank = 10)
            role1.save()
            self.stdout.write("\nRole 'administrateur' inserted.\n")
            role3 = members.Role(name='President', rank = 30)
            role3.save()
            self.stdout.write("Role 'président' inserted.\n")
            role4 = members.Role(name='Vice-president', rank = 40)
            role4.save()
            self.stdout.write("Role 'vice-président' inserted.\n")
            role5 = members.Role(name='Tresorier', rank = 50)
            role5.save()
            self.stdout.write("Role 'trésorier' inserted.\n")
            role6 = members.Role(name='Tresorier adjoint', rank = 60)
            role6.save()
            self.stdout.write("Role 'trésorier adjoint' inserted.\n")
            role7 = members.Role(name='Secretaire', rank = 70)
            role7.save()
            self.stdout.write("Role 'secrétaire' inserted.\n")
            role8 = members.Role(name='Secretaire adjoint', rank = 80)
            role8.save()
            self.stdout.write("Role 'secrétaire adjoint' inserted.\n")
            role9 = members.Role(name='Membre du bureau', rank = 90)
            role9.save()
            self.stdout.write("Role 'membre du bureau' inserted.\n")
            role10 = members.Role(name='Membre', rank = 100)
            role10.save()
            self.stdout.write("Role 'membre' inserted.\n")
            role11 = members.Role(name='Demandeur', rank = 110)
            role11.save()
            self.stdout.write("Role 'demandeur' inserted.\n")

            # apinc groups
            apinc_admin = groups.Group(name='apinc-admin', slug='apinc-admin')
            apinc_admin.email = "apinc-admin@apinc.org"
            apinc_admin.save()
            self.stdout.write("Group 'apinc-admin' inserted.\n")
            apinc_devel = groups.Group(name='apinc-devel', slug='apinc-devel')
            apinc_devel.email = "apinc-devel@apinc.org"
            apinc_devel.save()
            self.stdout.write("Group 'apinc-devel' inserted.\n")
            apinc_bureau = groups.Group(name='apinc-bureau', slug='apinc-bureau')
            apinc_bureau.email = "apinc-bureau@apinc.org"
            apinc_bureau.save()
            self.stdout.write("Group 'apinc-bureau' inserted.\n")
            apinc_secretariat = groups.Group(name='apinc-secretariat', slug='apinc-secretariat')
            apinc_secretariat.email = "apinc-secretariat@apinc.org"
            apinc_secretariat.save()
            self.stdout.write("Group 'apinc-secretariat' inserted.\n")
            apinc_tresorier = groups.Group(name='apinc-tresorier', slug='apinc-tresorier')
            apinc_tresorier.email = "apinc-tresorier@apinc.org"
            apinc_tresorier.save()
            self.stdout.write("Group 'apinc-tresorier' inserted.\n")
            apinc_contrib = groups.Group(name='apinc-contributeur', slug='apinc-contributeur')
            apinc_contrib.email = "apinc-contrib@apinc.org"
            apinc_contrib.save()
            self.stdout.write("Group 'apinc-contributeur' inserted.\n")
            apinc_membre = groups.Group(name='apinc-membre', slug='apinc-member')
            apinc_membre.email = "apinc-membre@apinc.org"
            apinc_membre.save()
            self.stdout.write("Group 'apinc-membre' inserted.\n")


            # Person
            laurent = members.Person()
            laurent.user = User.objects.create_user("laurent", "lau@apinc.org","laurent")
            laurent.user.is_staff = True
            laurent.user.is_superuser = True
            laurent.user.first_name = "Laurent"
            laurent.user.last_name = "Bives"
            laurent.user.save()
            laurent.sex = 'M'
            laurent.birth_date = date(1988,03,20)
#            laurent.country = france
            laurent.save()

            apinc_admin.add(laurent)
            apinc_devel.add(laurent)
            apinc_bureau.add(laurent)
            role1.add(laurent)
            role4.add(laurent)

            laurent_private = members.PersonPrivate()
            laurent_private.person = laurent
            laurent_private.notes = "Block de messages relatifs à l'utilisateur"
            laurent_private.save()
            self.stdout.write("Membre 'laurent' inserted.\n")

            pierre = members.Person()
            pierre.user = User.objects.create_user("pierre", "pierre@apinc.org","pierre")
            pierre.user.is_staff = False
            pierre.user.is_superuser = False
            pierre.user.first_name = "Pierre"
            pierre.user.last_name = "Nom_Pierre"
            pierre.user.save()
            pierre.sex = 'M'
            pierre.birth_date = date(1976,05,22)
#            pierre.country = france
            pierre.save()

            apinc_tresorier.add(pierre)
            apinc_devel.add(pierre)
            apinc_contrib.add(pierre)
            role1.add(pierre)

            pierre_private = members.PersonPrivate()
            pierre_private.person = pierre
            pierre_private.notes = "Block de messages relatifs à l'utilisateur"
            pierre_private.save()
            self.stdout.write("Membre 'pierre' inserted.\n")

            evariste = members.Person()
            evariste.user = User.objects.create_user("evariste", "evariste@apinc.org","evariste")
            evariste.user.is_staff = False
            evariste.user.is_superuser = False
            evariste.user.first_name = "evariste"
            evariste.user.last_name = "Nom_evariste"
            evariste.user.save()
            evariste.sex = 'M'
            evariste.birth_date = date(1976,05,22)
#            evariste.country = france
            evariste.save()

            apinc_devel.add(evariste)
            apinc_membre.add(evariste)
            role10.add(evariste)

            evariste_private = members.PersonPrivate()
            evariste_private.person = evariste
            evariste_private.notes = "Block de messages relatifs à l'utilisateur"
            evariste_private.save()
            self.stdout.write("Membre 'evariste' inserted.\n")
            # news
            news1 = news.News()
            news1.status = 1
            news1.body_html = "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lacinia \r\nvestibulum mollis. Sed non tempor est. Vestibulum vel mauris massa, ac \r\nhendrerit est. Integer scelerisque, ante at ultricies elementum, risus \r\norci bibendum arcu, non porta nisl diam in sapien. Vestibulum vitae sem a\r\n diam aliquam volutpat posuere non nisi. Nullam faucibus, neque id \r\nrutrum aliquam, nibh lorem condimentum dui, consequat lacinia ligula \r\nnisl ullamcorper nulla. In hac habitasse platea dictumst. Aliquam \r\nvulputate interdum eros, vitae eleifend mauris tincidunt sed. In vel \r\ntortor quis libero aliquet tempor eget in arcu. Ut sed neque quam. \r\nVivamus condimentum felis et justo vestibulum varius. Praesent egestas \r\ntincidunt leo, sed dictum metus vestibulum quis. Vestibulum sodales \r\nposuere aliquet. Vivamus suscipit nunc eu sem pulvinar volutpat. Nunc \r\nnon dui non enim tempor varius. Cum sociis natoque penatibus et magnis \r\ndis parturient montes, nascetur ridiculus mus. In eget urna id enim \r\niaculis elementum posuere nec mi. Curabitur a fringilla odio.</p>Ut vel dolor eget lectus tempus tempor in posuere mi. Sed purus ipsum, \r\nfringilla vel ullamcorper aliquet, iaculis non mi. Cras mi diam, \r\nultrices eget luctus non, congue eget nibh. Pellentesque vitae felis \r\nmetus, sed auctor dui. Nulla eget sem ligula. Cras sollicitudin eleifend\r\n lacus varius egestas. Pellentesque volutpat laoreet felis, porttitor \r\nconsectetur sem accumsan ut. Sed accumsan sem non mi suscipit molestie. \r\nFusce auctor tincidunt elit. Phasellus ut velit laoreet est sagittis \r\nvarius in et nunc. Proin scelerisque nisi eget orci sodales sit amet \r\ninterdum nulla tempus. Sed rutrum metus vel odio scelerisque eleifend. \r\nDuis nec libero elit. Donec non lorem ante. Suspendisse sagittis laoreet\r\n pulvinar. Nullam a eros id justo vestibulum aliquet viverra cursus \r\nvelit. Nam at malesuada purus.\r\n"
            news1.pub_date = datetime(2011,06,23,13,24,57)
            news1.slug = "nam-pulvinar-malesuada-dictum-nunc"
            news1.title = "Nam pulvinar malesuada dictum. Nunc."
            news1.save()
            self.stdout.write("News 1 inserted.\n")

            news2 = news.News()
            news2.status = 1
            news2.body_html = "<p>Nullam eget pharetra elit. Nam convallis scelerisque lorem ac volutpat. \r\nDonec vulputate orci accumsan urna iaculis blandit scelerisque est \r\ndictum. Nunc non nunc eros. Suspendisse ultricies felis et lorem gravida\r\n rhoncus. Ut euismod pulvinar mauris, eget lobortis quam ultrices et. \r\nDonec porttitor urna purus, ut varius sapien. Cras aliquet diam a lacus \r\nconsequat eleifend. Ut vel nisl odio. Cras nec risus ac ante mattis \r\ntempor. Cras malesuada mattis nisi, sit amet vehicula tellus ornare \r\nquis. In imperdiet mauris eu tellus convallis a eleifend neque posuere. \r\nNulla facilisis, lacus ut mollis auctor, neque sapien hendrerit elit, \r\neleifend euismod lacus tellus quis eros. Maecenas dui mi, pellentesque \r\nfeugiat feugiat vel, commodo id quam. Donec ornare iaculis augue id \r\nmalesuada. Aenean mattis condimentum mi ac porttitor. Fusce ultricies \r\ncursus viverra. Donec scelerisque tellus fringilla urna ornare sit amet \r\ntempor mauris ultrices.\r\n</p><ul><li>Cras luctus turpis at turpis euismod fringilla.</li><li>Integer et sapien eget est dignissim vulputate imperdiet eu neque.</li><li>Curabitur in tellus ligula, eget gravida mi.</li><li>Donec vel libero at quam gravida placerat.</li></ul>\r\n<p>\r\nProin feugiat nibh sed arcu lobortis ut varius diam feugiat. Suspendisse\r\n potenti. Maecenas convallis elit eget ligula scelerisque molestie. \r\nEtiam a sapien libero. Fusce vestibulum interdum lectus, in condimentum \r\nlibero placerat vel. Sed sit amet erat vitae neque venenatis pretium nec\r\n eu nisl. Praesent tempus est in justo pellentesque rhoncus. Nulla \r\nlaoreet metus id mauris feugiat vel aliquam metus pharetra. Phasellus \r\nmollis elementum turpis gravida ultricies. Sed tempus sollicitudin \r\nblandit. Nunc auctor dapibus ligula et scelerisque. Duis iaculis arcu \r\nnec purus molestie at tincidunt nisl fermentum. Vivamus eget vehicula \r\nmetus. Sed tincidunt arcu eu diam semper facilisis. Proin vitae dolor a \r\nodio pulvinar rutrum vitae a augue. Quisque semper facilisis mattis. \r\nDonec convallis facilisis justo, vel scelerisque est mattis eget. Sed \r\ncondimentum nibh id odio dignissim at tincidunt mi dapibus.\r\n</p>"
            news2.pub_date = datetime(2011,05,8,12,0,21)
            news2.slug = "aadipiscing-ultrices-vel-vel-massa"
            news2.title = "Aadipiscing ultrices vel vel massa"
            news2.save()
            self.stdout.write("News 2 inserted.\n")

            news3 = news.News()
            news3.status = 1
            news3.body_html = "<p>Phasellus ut magna velit. Pellentesque luctus metus id justo ullamcorper\r\n fringilla. Aenean scelerisque malesuada augue, in pulvinar diam pretium\r\n vel metus. </p><h3>Fusce enim massa</h3><p>Luctus a adipiscing at, viverra malesuada lorem. \r\nInteger viverra, nisi scelerisque volutpat varius, elit diam auctor \r\nmassa, quis venenatis eros orci vel felis. Donec sagittis lobortis \r\naugue, scelerisque posuere massa feugiat quis. Praesent suscipit dolor \r\nnon eros faucibus sagittis. Vestibulum vitae pellentesque eros. Morbi \r\nbibendum mauris eu erat rutrum molestie. Phasellus elementum pharetra \r\nnulla eget sollicitudin. Proin hendrerit ornare elit, eu cursus augue \r\nvestibulum sed. Cras eget purus at nisl viverra vestibulum id convallis \r\nquam. Quisque ornare justo nec ligula consequat tristique. Curabitur \r\nconvallis pulvinar ante ac auctor. In mattis varius massa, eget commodo \r\nipsum imperdiet vel. Integer vulputate scelerisque lorem, id tincidunt \r\nelit congue ut.</p>"
            news3.pub_date = datetime(2011,05,2,8,13,02)
            news3.slug = "nam-convallis"
            news3.title = "Nam convallis"
            news3.save()
            self.stdout.write("News 3 inserted.\n")

            news4 = news.News()
            news4.status = 1
            news4.body_html = "<h3>Vestibulum neque velit</h3><ul><li>Lobortis ut iaculis ut</li><li>Mollis nec turpis</li><li>Nulla\r\n a porta nisl.</li></ul><p>Nullam iaculis fringilla consequat. Aenean vel justo sit \r\namet leo semper ultrices et sit amet lorem. Ut ac dolor in massa \r\nultricies euismod non sit amet ligula. Nulla <strong>metus</strong> felis, placerat in \r\nsagittis eu, rhoncus sit amet risus. In eget <strong>lorem</strong> justo. Curabitur \r\nbibendum tristique enim, vel dapibus enim vehicula vel. In ornare \r\nlacinia lacus eget blandit. Ut<sup>id</sup> metus id velit interdum cursus. Nunc \r\nrutrum viverra nisl, eu elementum odio bibendum eget.&#160;\r\n  \r\n</p>"
            news4.pub_date = datetime(2011,04,18,13,24,11)
            news4.slug = "pellentesque-vestibulum-mattis-feugiat"
            news4.title = "Pellentesque vestibulum mattis feugiat"
            news4.save()
            self.stdout.write("News 4 inserted.\n")

            news5 = news.News()
            news5.status = 1
            news5.body_html = "<p><em>Morbi tellus risus</em>, euismod at pulvinar eget, interdum vel dolor. Aenean\r\n dictum condimentum interdum. Etiam a erat massa. Sed fermentum porta \r\nconvallis. <strong>Nam eget dolor in magna porta sagittis id sed elit.</strong> Fusce \r\nlaoreet massa diam, in placerat ipsum. Donec pharetra tempus convallis. \r\nAenean sit amet dolor ante, sit amet fringilla ligula. Mauris porta, \r\nlectus ac lobortis tincidunt, mauris lacus laoreet est, vitae cursus \r\nfelis lacus a elit. Pellentesque ut purus et augue hendrerit aliquam et \r\nsit amet est. </p><blockquote><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur \r\nsuscipit posuere purus, vel tempus turpis aliquet id.</p></blockquote>"
            news5.pub_date = datetime(2011,04,14,4,54,17)
            news5.slug = "morbi-tellus-risus"
            news5.title = "Morbi tellus risus"
            news5.save()
            self.stdout.write("News 5 inserted.\n")

            news6 = news.News()
            news6.status = 0 
            news6.body_html = "<div><h2>Neque porro quisquam</h2><ol><li>Sed eget massa condimentum justo pellentesque gravida.</li><li>Aliquam lobortis eros non justo aliquam sed cursus turpis porta.</li><li>Donec tincidunt aliquet dolor, vel tempus est hendrerit eget.</li></ol><h3><em>est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...</em></h3>"
            news6.pub_date = datetime(2010,02,15,9,35,02)
            news6.slug = "neque-porro-quisquam"
            news6.title = "Neque porro quisquam"
            news6.save()
            self.stdout.write("News 6 inserted.\n")

            news7 = news.News()
            news7.status = 1
            news7.body_html = "<div><h2>Lorem ipsum</h2><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam id hendrerit mi. Vivamus placerat turpis non turpis commodo posuere. <strong>Vivamus</strong> cursus bibendum iaculis. In rutrum sem non lorem malesuada in gravida leo adipiscing. Nullam ultrices bibendum pretium. Aenean condimentum, ipsum et imperdiet fringilla, magna ipsum interdum ligula, eget condimentum lacus tellus a leo. Curabitur imperdiet consequat nulla, sed rhoncus eros porttitor a. Pellentesque vel purus ut neque vehicula mollis sed ut metus. Ut interdum aliquet blandit. In urna eros, sollicitudin eu eleifend ac, mollis nec lectus. In interdum pretium <strong>venenatis</strong>. Vestibulum venenatis, risus sed rutrum elementum, justo leo gravida purus, id porttitor est tellus sed ante. Maecenas et dapibus dolor. Curabitur pulvinar, leo nec imperdiet porttitor, odio quam gravida lacus, vitae tincidunt dolor neque ut enim. In <sup>gravida</sup>, nibh ut molestie sagittis, arcu sem laoreet quam, in vehicula quam neque a risus.</p><h2>Ut interdum aliquet blandit</span></h2></div></span><div></span><div><ul><li>In eu quam et tortor mollis facilisis ut varius ipsum.</li><li>Quisque condimentum porta nibh, in congue nulla iaculis eu.</li></ul><h3>Quisque dignissim scelerisque felis, sit amet tempor justo vehicula eget.</span></h3><ul><li>Phasellus non justo neque, quis mollis lorem.</li><li>Maecenas vehicula iaculis elit, nec tempor urna elementum bibendum.</li></ul><p>Suspendisse nec mi diam, a viverra ligula. Quisque iaculis arcu eu lectus egestas malesuada egestas ac eros. Maecenas dignissim quam tincidunt quam tincidunt et tincidunt orci malesuada. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse at ante ligula, in interdum erat. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.</p><blockquote><p>Sed id lacus nibh, ac dictum nisi. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sit amet lorem et lorem suscipit ultricies venenatis non justo. Aenean cursus facilisis elit a feugiat. Mauris lacus diam, convallis et vulputate ut, dapibus eu lectus. In arcu quam, pharetra in egestas vitae, ultrices et urna. Nunc lobortis bibendum diam vitae venenatis. Ut scelerisque, risus sit amet tincidunt placerat, sapien massa ultricies odio, ut blandit lectus nulla eget neque.</p></blockquote></div></span></div>"
            news7.pub_date = datetime(2010,9,07,22,00,32)
            news7.slug = "vivamus-cursus-bibendum-iaculis"
            news7.title = "Vivamus cursus bibendum iaculis"
            news7.save()
            self.stdout.write("News 7 inserted.\n")

            news8 = news.News()
            news8.status = 0 
            news8.body_html = "Vivamus vehicula feugiat lacus id sagittis. Phasellus venenatis vulputate velit non pellentesque. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse nisi enim, scelerisque at ullamcorper id, pharetra id magna. Suspendisse augue neque, faucibus nec interdum vitae, lacinia quis justo. Nullam a magna mi. Etiam hendrerit diam ut ipsum dignissim lacinia. Fusce porttitor erat eu urna porta ac tempor sapien ullamcorper. Aliquam magna massa, placerat at imperdiet at, volutpat consectetur lectus. Nulla iaculis adipiscing commodo. Pellentesque eu purus volutpat felis suscipit porttitor. In dapibus, ligula molestie fringilla posuere, mi leo laoreet enim, vitae congue purus nisl vel diam. Ut tempus sapien lacinia neque viverra at commodo orci interdum. Vivamus pellentesque pellentesque scelerisque. Mauris varius varius velit eget fermentum. Duis auctor tortor eu dui dignissim porta."
            news8.pub_date = datetime(2011,01,13,23,12,37)
            news8.slug = "vivamus-vehicula"
            news8.title = "Vivamus vehicula"
            news8.save()
            self.stdout.write("News 8 inserted.\n")

            self.stdout.write('Successfully filled database\n')

        except Exception, e:
            # TODO Error message handling
            raise CommandError('Filldb "%s"' % e)
