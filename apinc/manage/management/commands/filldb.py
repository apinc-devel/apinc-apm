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
            self.stdout.write("Homepage pseudo-static page inserted.\n")

            about = pages.TextBlock(slug="about", title="About page title")
            about.body_html = "Contenu de la page à propos."
            about.save()
            self.stdout.write("About pseudo-static page inserted.\n")

            legal_notice = pages.TextBlock(slug="legal-notice", title="Legal notice and terms of use")
            legal_notice.body_html = "<p>L'Association pour la promotion de l'Internet Non Commercial est une association de loi 1901.</p>\r\n<h3>Siège social</h3><p>Association APINC - Federation Française des Clubs Unesco<br />173 rue de Charenton<br />75012 PARIS<br />FRANCE</p>"
            legal_notice.save()
            self.stdout.write("Legal notice pseudo-static page inserted.\n")

            contact = pages.TextBlock(slug="contact", title="Contact page title")
            contact.body_html = "Contenu de la page des contacts."
            contact.save()
            self.stdout.write("Contact pseudo-static page inserted.\n")

            association = pages.TextBlock(slug="association", title="The association")
            association.body_html = "<p>L'Association APINC a pour but duis euismod convallis orci et lacinia. In gravida consectetur felis, id gravida enim eleifend at. Aliquam erat volutpat. Vestibulum eget est turpis, ut porta arcu. Ut commodo pellentesque risus, ac hendrerit leo placerat sit amet. Nulla blandit malesuada tortor, in auctor leo mollis eu. Donec ac auctor velit. Vestibulum vel ultrices sapien. Nam fermentum facilisis arcu, vitae tempus sapien suscipit vitae. Nam molestie suscipit erat id faucibus.</p>"
            association.save()
            self.stdout.write("Association pseudo-static page inserted.\n")

            status = pages.TextBlock(slug="status", title="Status de l'association")
            status.body_html = "<p>Il est fondé entre les adhérents aux présents statuts une association régie par la Loi du 1<sup>er</sup>&#160;juillet 1901 et le décret du 16 août 1901, ayant pour titre&#160;: APINC dont la signification est&#160;: Association Pour l'Internet Non Commercial.</p><h2>Objet</h2><p>Cette association a pour but de défendre et promouvoir l'Internet universitaire et/ou non commercial et de proposer des services associatifs autogérés tels qu'hébergement et prestations liées à Internet. Elle pourra, en outre, se consacrer à toute activité liée aux technologies de l'information, notamment en matière de formation, de diffusion des connaissances et de réalisations liées à Internet.</p><h2>Siège social</h2><p>Le siège social est fixé au domicile du Président.</p><p>Il pourra être transféré par simple décision du conseil d'administration, la ratification par l'Assemblée Générale est nécessaire.</p><h2>Durée</h2><p>Sa durée est illimitée.</p><h2>Les membres</h2><p>L'association se compose :</p><ul><li>De membres fondateurs<br />Sont considérés comme tels les premiers signataires des présents statuts qui ont renouvelé leur adhésion à l'association sans interruption depuis sa création. Un membre fondateur n'ayant pas renouvelé son adhésion ou ayant décidé de quitter l'association, ne peut prétendre par la suite rejoindre le collège des membres fondateurs. Il lui demeure possible d'adhérer à l'association dans les autres collèges, la procédure courante lui est alors appliquée.</li><li>De membres actifs<br />Sont considérés comme tels, après acceptation conformément à l'article VI, les personnes physiques ou morales qui participent effectivement au fonctionnement de l'association et des services qu'elle propose et qui auront versé une cotisation annuelle dont le montant est fixé par l'article VII.</li><li>De membres bienfaiteurs<br />Sont considérés comme tels, les personnes physiques ou morales qui, souhaitent soutenir financièrement l'association, et qui auront versé une fois au moins, une cotisation annuelle d'un montant supérieur ou égal à vingt fois le montant traditionnel.</li><li>De membres d'honneurs<br />Sont considérés comme tels, les personnes qui ont rendu des services signalés à l'association ; ils sont dispensés de cotisation.</li></ul><h2>Conditions d'adhésion</h2><p>Les demandes d'adhésion sont formulées par écrit ou en ligne par le demandeur et acceptées par le conseil d'administration lequel, en cas de refus, n'a pas à faire connaître les raisons.</p><h2>Cotisation</h2><p>Pour faire partie de l'association, il faut être à jour de sa cotisation dont le montant est déterminé annuellement par l'Assemblée Générale.</p><h2>Qualité de membre</h2><ul><li>la démission,</li><li>le décès,</li><li>la radiation prononcée par le Conseil d'Administration pour non-paiement de la cotisation ou pour motif grave, l'intéressé ayant été invité par lettre recommandée à se présenter devant le bureau pour fournir des explications.</li></ul><h2>Ressources</h2><p>Les ressources de l'association se composent :</p><ul><li>des dons et cotisations de ses membres ;</li><li>du revenu de ses biens ;</li><li>des sommes perçues en contrepartie des prestations fournies par l'association ;</li><li>des subventions qui pourraient lui être accordées par l'État ou les collectivités publiques ;</li><li>de toutes autres ressources autorisées par les textes législatifs et réglementaires.</li></ul><p>Afin de préserver l'indépendance de l'association, le Conseil d'Administration devra donner son accord avant acceptation de ressources autres que les cotisations et dons des membres de l'association.</p><h2>Bureau</h2><p>L'association est dirigée par un conseil de 2 membres minimum, élus pour deux années par l'Assemblée Générale. Les membres sont rééligibles.</p><p>Le conseil d'administration choisit parmi ses membres, au scrutin secret, un bureau composé de :</p><ul><li>un président,</li><li>un trésorier,</li></ul><p>auxquels peuvent être associés :</p><ul><li>un secrétaire,</li><li>un (ou des) vice-président(s),</li><li>un trésorier adjoint,</li><li>un secrétaire adjoint.</li></ul><p>En cas de vacances, le conseil pourvoit provisoirement au remplacement de ses membres. Il est procédé à leur remplacement définitif par la plus prochaine Assemblée Générale. Les pouvoirs des membres ainsi élus prennent fins à l'époque où devrait normalement expirer le mandat des membres remplacés.</p><h2>Rapport annuel</h2><p>Le Bureau garantit l'existence annuelle du rapport d'activité et du rapport financier de l'association, qui sont préparés par le trésorier et le secrétaire. C'est l'assemblée générale qui valide ces documents à chaque fin d'exercice.</p><h2>Règlement intérieur</h2><p>L'association se dote d'un règlement intérieur, qui définit les règles en vigueur concernant les prises de décisions inhérentes au fonctionnement de l'APINC, ainsi que toutes modalités additionnelles de désignation et de révocation de membres ou groupes de membres à qui l'association délègue certaines responsabilités. Ce règlement intérieur peut évoluer sur proposition d'un groupe de travail spécifique de l'association, après vote à la majorité relative de l'assemblée générale.</p><h2>Réunion du bureau</h2><p>Le conseil se réunit deux fois par an au moins et chaque fois qu'il est convoqué par son président ou sur la demande de la moitié de ses membres. Les réunions du Conseil d'Administration peuvent se tenir sans que tous ses membres se trouvent physiquement réunis dans la mesure ou des moyens de communications en temps réel écrits, sonores et/ou visuels sont mis en place dans des conditions définies dans le Règlement Intérieur.</p><p>Il est tenu un procès-verbal des séances.</p><p>Les procès-verbaux sont signés par le président et le vice-président chargé des questions administratives ; ils sont inscrits sur un registre coté et paraphé par le représentant de l'association.</p><p>Sauf dispositions particulières inscrites dans les statuts concernant certaines décisions, les décisions sont prises à la majorité absolue : en cas de partage, la voix du président est prépondérante.</p><h2>Assemblée Générale Ordinaire</h2><p>L'Assemblée Générale Ordinaire comprend tous les membres de l'association. Elle est réunie chaque année. Quinze jours au moins avant la date fixée, les membres de l'association sont convoqués par le Président. L'ordre du jour est obligatoirement indiqué sur les convocations et ne devront être traitées, lors de l'Assemblée Générale, que les questions soumises à l'ordre du jour. Les convocations pourront être envoyées par les moyens de communication électronique tels que le courrier électronique.</p><p>Le président assisté des membres du bureau, préside l'Assemblée Générale. La situation morale de l'association est exposée et approuvée par l'Assemblée.</p><p>Le trésorier rend compte de sa gestion et soumet le bilan à l'approbation de l'Assemblée.</p><p>Il est procédé, lorsque cela est prévu, après épuisement de l'ordre du jour, au remplacement au scrutin secret, des membres du conseil sortant.</p><h2>Assemblée Générale Extraordinaire</h2><p>Si besoin est, pour toute modification des statuts ou sur la demande de la moitié plus un des membres inscrits, le président peut convoquer une Assemblée Générale Extraordinaire, suivant les formalités prévues par l'article XIV.</p><h2>Quorum</h2><p>Tout vote proposé à l'assemblée générale, qu'il soit proposé par le comité exécutif ou qu'il s'agisse d'un vote de révocation, nécessite la participation minimale de 30% des adhérents.</p><h2>Dissolution</h2><p>En cas de dissolution prononcée par les deux tiers au moins des membres présents à l'Assemblée Générale, un ou plusieurs liquidateurs son nommés par celle-ci et l'actif, s'il y a lieu, est dévolu conformément à l'article 9 de la Loi du 1er juillet 1901 et au décret du 16 août 1901.</p><p><em>Fait à Paris, le 19 décembre 2001</em></p>"
            status.save()
            self.stdout.write("Status pseudo-static page inserted.\n")

            charter = pages.TextBlock(slug='charter', title="Charte d'utilisation des services")
            charter.body_html = "<p>Révision 0.81 16/11/2006</p><h2>Objet</h2><p>Ce texte a pour but d'imposer des règles de bonne conduite à l'ensemble des membres du réseau APINC afin d'en assurer la fiabilité.</p><p>Tous les membres doivent respecter à ces règles. Tout manquement est susceptible de l'émission d'un avertissement pouvant entraîner la fermeture du compte concerné, si celui ci ne s'y conforme pas dans un délai de 10 jours après approbation de l'association via un vote associatif general</p><h2>Devoirs et droits des membres</h2><p>Tous les membres ont un droit de regard sur les informations les concernant. APINC n'utilise pas les données personnelles de ses membres à des fins publicitaires ou commerciales.</p><p>Les membres ont un droit de participation à la vie de la communauté APINC et d'intervention dans les décisions importantes du réseau. Ils se doivent de participer à la vie du serveur.</p><p>Les administrateurs d'APINC se doivent d'écouter et répondre à ses membres et de donner leur avis sur toutes suggestions données par les membres.</p><p>Les membres d'APINC se doivent de signaler tout problème lié au fonctionnement du serveur ou à sa sécurité.</p><p>Les membres d'APINC se doivent d'indiquer des coordonnées correctes lors de l'inscription</p><p>Les membres d'APINC se doivent de respecter la législation de&#160; leurs pays de résidence et de veiller à ne pas utiliser trop de ressources sur les serveurs de l'association.</p><h2>Utilisation du compte</h2><p>Le compte UNIX de base est fixe à 200 Mo.</p><p>Le compte peut être utilisé pour les fins suivantes&#160;:</p><ul><li>réception et émission d'emails,</li><li>publication de pages Internet,</li><li>stockage de données privées.</li></ul><p>Les services autorisés sont les suivants&#160;:</p><ul><li>pop (réception du courrier),</li><li>smtp (émission de courrier) sur le réseau interne d'APINC,</li><li>http (pages Internet hébergées sur APINC),</li><li>ftp personnel (transfert de fichiers sur le serveur APINC),</li></ul><p>Pour le PHP et les scripts CGI&#160;:</p><ul><li>Les fonctions mail() et fopen() sont autorisées (tout abus entraînera la fermeture définitive de l'utilisation de ces fonctions).</li><li>Les autres fonctions sont également autorisées sauf si elles ne sont pas accessibles en safe_mode.</li><li>Vous devez faire attention au temps d'exécution de vos scripts et de veiller à ne pas trop utiliser de ressources sur les serveurs de l'association</li></ul><p>Tout service non explicitement cité ci-dessus n'est pas autorisé sur le réseau d'APINC.</p><h2>Identifiant et mot de passe</h2><p>Le mot de passe donné lors de l'inscription est strictement personnel et ne doit pas être divulgué même à l'assistance technique d'APINC. Il ne peut pas etre personnalisable</p><p>APINC ne peut pas être tenu responsable en cas de perte de données due à une divulgation du mot de passe.</p><p>Vous pouvez demander à changer de mot de passe, il vous sera attribué un nouveau mot de passe généré par APINC.</p><h2>Compte ftp personnel</h2><p>Ce service est strictement personnel et ne doit pas servir à la publication de données publiques. Toute utilisation du service FTP personnel accordée aux membres du réseau APINC à des fins de publication de données pirates et ou non autorisées par les lois du pays de résidence du membre, entraînera un avertissement pouvant donner lieu à la fermeture définitive du compte, si celui-ci n'est pas mis en conformité.</p><p>Les uploads massifs sur le serveurs FTP (webcam) ne sont pas autorises</p><p>Les fichiers MP3 ne sont pas autorisés sauf si vous en êtes l'auteur&#160;; nous recommandons vivement le format libre OGG.</p><p><strong>Les fichiers binaires (exécutables et librairies) ne sont pas autorisés sauf si vous y incluez les sources, et qu'elles soient publies sous licence GPL ou compatible.</strong></p><h2>Pages Internet hébergées par APINC (service HTTP)</h2><p>La priorité est donnée aux sites Internet lies aux logiciels libres et aux sites associatifs étant donné la philosophie et la spécialisation d'APINC. APINC n'héberge que des sites Internet non commerciaux. Le service d'hébergement n'est ouvert qu'aux adhérents de l'association. Cependant un délai de 10 jours est donné aux nouveaux membres du service d'hébergement pour se mettre à jour de la cotisation à l'association APINC. Le prix de l'adhésion est fixé à 14&#160;EUR/an et permet de prendre en charge les frais de renouvellement du materiel informatique et les frais de bande passante. Les membres hors France ou ne pouvant pas émettre un chèque francais doivent s'acquitter de la cotisation via un paiement Paypal a l'adresse paypal@apinc.org, ou par virement (contacter pour cela tresorier_AT_apinc.org).</p><p>Les membres d'APINC sélectionnent les sites Internet, la décision d'hébergement d'un site Internet relève de la seule et unique décision des membres d'APINC.</p><p>Tout site Internet hébergé par APINC doit être conforme à la présente charte, dans le cas contraire, un avertissement sera envoyé et le membre aura un délai de 10 jours pour y apporter les modifications nécessaires, sinon le compte concerné sera fermé.</p><p>L'ensemble des sites Internet&#160;<strong>DOIVENT</strong>&#160;etre conforme a la description initiale du projet décrit lors de l'inscription. Le sous-hebergement (utiliser les serveurs APINC pour heberger d'autres personnes avec son compte) est strictement interdit et provoquera la fermeture définitive et immediate du compte</p><p>Les administrateurs peuvent demander aux membres de statuer sur le refus d'une demande d'inscription, conformément à la politique de sélection des sites Internet hébergés par APINC.</p><p>Vous devez respecter la législation en vigueur dans votre pays de résidence ainsi que la législation française vis à vis des données électroniques.</p><p>Vous devez également respecter les droits d'auteur sur tous les types de format électronique (musique, photos, images, textes, logiciels ...).</p><p>Vous devez veiller à la légèreté de vos pages Internet afin d'éviter la saturation des serveurs et de la bande passante. APINC est un service collectif et par conséquent chaque membre doit veiller à ne pas détériorer la qualité du service. Tout site utilisant trop de bande passante entraînera un avertissement pour lequel le membre aura 10 jours pour effectuer les modifications nécessaires.</p><p>Le service d'hébergement de l'association APINC n'impose pas de publicité, nous vous demandons par conséquent de ne pas ajouter de bannières publicitaires sur votre site Internet, étant donné l'aspect non commercial de ce service. En cas de manquement, seul un vote associatif permet l'emission d'un avertissement au webmaster concerne.</p><p>Tout lien vers un ou des sites illégaux est également interdit.</p><p>Tout site pornographique, érotique et/ou ayant un contenu réservé à un public majeur ne pourra pas être accepté et sera fermé sans préavis.</p><p>Note vis à vis de l'utilisation des CGI et du PHP sur APINC&#160;:</p><p>Nous vous conseillons fortement de n'utiliser que les scripts recommandés par les administrateurs.</p><p>Les scripts de chat (phpmychat par exemple) sont interdit, ainsi que les CGI::IRC pour des raisons de securite et d'utilisation de ressources</p><p>Les connexions MySQL persistantes ne sont pas autorises. On evitera egalement l'utilisation de requetes DELAYED, en particulier pour SPIP (ancienne version 1.4), on utilisera une version patchee. Il est quand meme plus simple d'utiliser la derniere version.</p><p>Vous devez veiller à la stabilité de vos scripts.</p><h2>Emails (service POP et SMTP)</h2><p>Vous ne devez pas utiliser votre compte email afin d'envoyer des courriers non sollicités et pour des fins d'envoi de courrier en masse.</p><p>Tout site surpris à utiliser frauduleusement le service SMTP pour des envois de courrier en masse recevra un avertissement qui donnera lieu à la fermeture définitive du compte en cas de récidive ou si cette action n'a pas été justifiée.</p><p>L'envois d'email via le protocole ESMTP authentifie est autorise</p><p>Si vous devez envoyer un grand nombre d'emails (ex&#160;: mailing-listes) Utilisez de preference les mailing-listes SYMPA du service APINC et non pas des scripts de mailing listes codes en php.</p><p>Un quota de 100 Mo est appliqué pour chaque boite aux lettres électronique.</p><h2>Interruptions de service</h2><p>APINC ne peut être tenue responsable d'interruptions momentanées ou lenteurs de service causant ou non des pertes financières.</p><p>En cas de fermeture définitive du service APINC, tous les membres seront avertis par email 10 jours minimum avant la fermeture effective et seront libres de récupérer leurs données via téléchargement pendant ce délai.</p><p>APINC ne pourra être tenue responsable en cas de difficultés pour le membre à récupérer ses données durant ce délai. Ces données seront alors détruites.</p><h2>Responsabilité d'APINC</h2><p>APINC ne peut en aucun cas être tenue responsable du contenu des sites et/ou des fichiers hébergés sur les serveurs. Ces sites et ou fichiers restent sous l'entière responsabilité de leurs propriétaires respectifs.</p><p>Les administrateurs d'APINC se réservent le droit de modifier la présente charte après consultation et approbation des membres. La modification de la charte prendra effet 5 jours après son approbation et l'ensemble des membres devra s'y conformer durant ce délai.</p>"
            charter.save()

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


            # Person
            laurent = members.Person()
            laurent.user = User.objects.create_user("laurent", "lau@a.org","laurent")
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

            laurent_private = members.PersonPrivate()
            laurent_private.person = laurent
            laurent_private.notes = "Block de messages relatifs à l'utilisateur"
            laurent_private.save()

            member_laurent = members.Member(person=laurent)
            member_laurent.save()

            self.stdout.write("Membre 'laurent' inserted.\n")

            stephane = members.Person()
            stephane.user = User.objects.create_user("stephane", "c@a.org","stephane")
            stephane.user.is_staff = False
            stephane.user.is_superuser = False
            stephane.user.first_name = "Stephane"
            stephane.user.last_name = "Kanshine"
            stephane.user.save()
            stephane.sex = 'M'
            stephane.birth_date = date(1976,05,22)
#            stephane.country = france
            stephane.save()

            apinc_tresorier.add(stephane)
            apinc_devel.add(stephane)
            apinc_contrib.add(stephane)

            stephane_private = members.PersonPrivate()
            stephane_private.person = stephane
            stephane_private.notes = "Block de messages relatifs à l'utilisateur"
            stephane_private.save()

            member_stephane = members.Member(person=stephane)
            member_stephane.save()
            role_president.add(member_stephane)

            self.stdout.write("Membre 'stephane' inserted.\n")

            mathieu = members.Person()
            mathieu.user = User.objects.create_user("mathieu", "m@a.org","mathieu")
            mathieu.user.is_staff = False
            mathieu.user.is_superuser = False
            mathieu.user.first_name = "Mathieu"
            mathieu.user.last_name = "Pillard"
            mathieu.user.save()
            mathieu.sex = 'M'
            mathieu.birth_date = date(1976,05,22)
#            mathieu.country = france
            mathieu.save()

            apinc_tresorier.add(mathieu)
            apinc_devel.add(mathieu)
            apinc_contrib.add(mathieu)

            mathieu_private = members.PersonPrivate()
            mathieu_private.person = mathieu
            mathieu_private.notes = "Block de messages relatifs à l'utilisateur"
            mathieu_private.save()

            member_mathieu = members.Member(person=mathieu)
            member_mathieu.save()
            role_vice_president.add(member_mathieu)

            self.stdout.write("Membre 'mathieu' inserted.\n")

            gregory = members.Person()
            gregory.user = User.objects.create_user("gregory", "g@r.net","gregory")
            gregory.user.is_staff = False
            gregory.user.is_superuser = False
            gregory.user.first_name = "Gregory"
            gregory.user.last_name = "Auzanneau"
            gregory.user.save()
            gregory.sex = 'M'
            gregory.birth_date = date(1976,05,22)
#            gregory.country = france
            gregory.save()

            apinc_devel.add(gregory)
            apinc_membre.add(gregory)

            gregory_private = members.PersonPrivate()
            gregory_private.person = gregory
            gregory_private.notes = "Block de messages relatifs à l'utilisateur"
            gregory_private.save()

            member_gregory = members.Member(person=gregory)
            member_gregory.save()
            role_tresorier.add(member_gregory)

            self.stdout.write("Membre 'gregory' inserted.\n")

            olivier = members.Person()
            olivier.user = User.objects.create_user("olivier", "o@c.org","olivier")
            olivier.user.is_staff = False
            olivier.user.is_superuser = False
            olivier.user.first_name = "Olivier"
            olivier.user.last_name = "Tronel"
            olivier.user.save()
            olivier.sex = 'M'
            olivier.birth_date = date(1972,04,12)
#            olivier.country = france
            olivier.save()

            apinc_devel.add(olivier)
            apinc_membre.add(olivier)

            olivier_private = members.PersonPrivate()
            olivier_private.person = olivier
            olivier_private.notes = "Block de messages relatifs à l'utilisateur"
            olivier_private.save()

            member_olivier = members.Member(person=olivier)
            member_olivier.save()
            role_secretaire.add(member_olivier)

            self.stdout.write("Membre 'olivier' inserted.\n")

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
            news6.body_html = "<div><h2>Neque porro quisquam</h2><ol><li>Sed eget massa condimentum justo pellentesque gravida.</li><li>Aliquam lobortis eros non justo aliquam sed cursus turpis porta.</li><li>Donec tincidunt aliquet dolor, vel tempus est hendrerit eget.</li></ol><h3><em>est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...</em></h3></div>"
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
