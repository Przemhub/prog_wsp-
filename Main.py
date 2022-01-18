import sys
from random import randrange

import pygame

from LoadBalancer import MyLoadBalancer
from MyFile import MyFile


class Interface:
    def __init__(self):
        pygame.init()

        pygame.display.init()
        resolution = (1450, 800)
        self.screen = pygame.display.set_mode(resolution)

        self.DIR_NUMBER = 5
        self.CLIENTS_NUMBER = 0
        self.client_list = []
        self.load_balancer = MyLoadBalancer()
        self.load_balancer.start()
        self.init_objects()
        self.init_texts()

        self.loop()

    def init_objects(self):
        self.dir_rects = []
        for i in range(0, self.DIR_NUMBER):
            self.dir_rects.append(pygame.rect.Rect(i * self.screen.get_width() / self.DIR_NUMBER, 0,
                                                   self.screen.get_width() / self.DIR_NUMBER,
                                                   self.screen.get_height() / 5))

        self.client_rects = []
        self.client_text_rects = []

        self.button_image = pygame.image.load("resources/button_dodaj.png")
        self.button_rect = pygame.rect.Rect(10,200,self.button_image.get_width(),self.button_image.get_height())

    def reset_client_text(self):

        self.clients = [self.font.render("Client " + str(i + 1), True, (0, 0, 0)) for i in
                        range(0, self.CLIENTS_NUMBER)]
        self.client_file_sizes = []
        for i in range(0, self.CLIENTS_NUMBER):
            self.client_file_names.append(
                [self.font.render(file.name, True, (0, 0, 0)) for file in self.client_list[i][1]])
            self.client_file_sizes.append(
                [self.font.render(str(file.size), True, (0, 0, 0)) for file in self.client_list[i][1]])
            self.client_text_rects.append(
                pygame.Rect(self.dir_rects[i].midbottom[0], self.dir_rects[0].bottom + 50 + i * 30, 0, 0))

    def reset_dir_texts(self):
        self.progresses = []
        self.file_names = []
        for directory in self.load_balancer.directories:
            self.progresses.append(self.font.render(str(directory.progress) + "%", True, (0, 0, 0)))
            self.file_names.append(self.font.render(str(directory.client_name), True, (0, 0, 0)))

    def init_texts(self):
        self.font = pygame.font.SysFont("Calibri", 24, True)
        self.dirs = [self.font.render("Dir " + str(i + 1), True, (0, 0, 0)) for i in
                     range(0, self.DIR_NUMBER)]
        self.clients = [self.font.render("Client " + str(i + 1), True, (0, 0, 0)) for i in
                        range(0, self.CLIENTS_NUMBER)]
        self.progresses = []
        self.file_names = []
        self.client_file_names = []
        self.client_file_sizes = []
        for directory in self.load_balancer.directories:
            self.progresses.append(self.font.render(str(directory.progress), True, (0, 0, 0)))
            self.file_names.append(self.font.render(str(directory.file_name), True, (0, 0, 0)))

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                self.handle_button_click(event)
            self.screen.fill((255, 255, 255))
            self.reset_dir_texts()
            self.draw()
            pygame.display.flip()

    def draw(self):
        for i in range(0, self.DIR_NUMBER):
            pygame.draw.rect(self.screen, (255, 255, 255), self.dir_rects[i])
            pygame.draw.rect(self.screen, (0, 0, 0), self.dir_rects[i], 3)
            self.screen.blit(self.dirs[i], self.dir_rects[i].move(40, 20))
            self.screen.blit(self.file_names[i], self.dir_rects[i].move(40, 70))
            self.screen.blit(self.progresses[i], self.dir_rects[i].move(120, 120))
        for i in range(0, self.CLIENTS_NUMBER):
            self.screen.blit(self.clients[i], self.client_text_rects[0].move(0, 40 * i))
            for j in range(0, len(self.client_file_sizes[i])):
                self.screen.blit(self.client_file_sizes[i][j],
                                 self.client_text_rects[0].move(140 + j * 100,  i * 40))
        self.screen.blit(self.button_image, self.button_rect)

    def handle_button_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                self.incr_clients()

    def incr_clients(self):
        self.CLIENTS_NUMBER += 1
        self.client_rects.append(pygame.rect.Rect(0,
                                                  self.dir_rects[0].bottom + (
                                                          (self.CLIENTS_NUMBER - 1) * self.screen.get_height() / 4),
                                                  self.screen.get_width(),
                                                  self.screen.get_height() / 4))

        self.client_list.append(self.generate_client())
        self.reset_client_text()

    def generate_client(self):
        r = randrange(0, 255)
        g = randrange(0, 255)
        b = randrange(0, 255)
        files = []
        files_num = randrange(0, 20)
        for i in range(0, files_num):
            files.append(MyFile("file" + str(i), randrange(1000, 15000), "client"+str(self.CLIENTS_NUMBER)))
        print("client", self.CLIENTS_NUMBER, "amount of files:", len(files))
        self.load_balancer.add_files(files)
        self.reset_dir_texts()
        return ["client" + str(self.CLIENTS_NUMBER), files, (r, g, b)]


if __name__ == "__main__":
    Interface()
